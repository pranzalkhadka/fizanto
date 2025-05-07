from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext, MessageFactory
from botbuilder.schema import Activity, ActivityTypes
from dotenv import load_dotenv
import os
from agno.models.groq import Groq
from agno.agent import Agent
from agno.team import Team
from agno.vectordb.lancedb import LanceDb
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.agent import Agent, AgentKnowledge
from typing import List, Dict, Optional, Tuple
import re
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools import tool
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
APP_ID = os.getenv('APP_ID')
APP_PASSWORD = os.getenv('APP_PASSWORD')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = BotFrameworkAdapterSettings(app_id=APP_ID, app_password=APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)


EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="memoryy/lancedb",
        table_name="email_memory",
        embedder=FastEmbedEmbedder(id="BAAI/bge-small-en-v1.5")
    )
)

memory_db = SqliteMemoryDb(table_name="memory", db_file="/home/pranjal/Downloads/fizanto/memoryy/memory_session.db")
memory = Memory(db=memory_db)

user_id = "jon_hamm@example.com"
session_id = "1001"


def extract_email_metadata():

    session_summary = memory.get_session_summary(
    user_id=user_id, session_id=session_id)

    # query = "Email about Lending Club Risk Management"

    results = knowledge_base.search(session_summary.summary)

    content = results[0].content

    sender_match = re.search(r"Received an email from (.+?) <(.+?)>", content)
    sender_name = sender_match.group(1) if sender_match else None
    recipient = sender_match.group(2) if sender_match else None

    subject_match = re.search(r"subject (.+?) at", content)
    subject = subject_match.group(1).strip()

    message_id_match = re.search(r"identified as <(.+?)>", content)
    message_id = message_id_match.group(1) if message_id_match else None
        
    return recipient, subject, message_id


@tool(
    name="send email",
    description="Send an email",
    show_result=True,
    stop_after_tool_call=True,
    cache_results=False
)
def send_email():
    """
    Use this function to send an email.
    """
    recipient, subject, message_id = extract_email_metadata()

    reply_body = "Thank you for your email. I will get back to you shortly."

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = "Re: " + subject
        msg['In-Reply-To'] = message_id
        msg['References'] = message_id
        msg.attach(MIMEText(reply_body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        
        return "Email sent sucessfully"
        
    except: 
        return "Failed to send an email"


email_agent = Agent(
    name="Send Email",
    # description="You are an expert in sending emails.",
    # model=OpenRouter(id="gpt-4o"),
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[send_email],
    instructions=["Call the send_email tool to send an email"],
    show_tool_calls=True,
    markdown=True
)


knowledge_agent = Agent(
    name="Knowledge Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    # model=OpenRouter(id="gpt-4o"),
    description="You are an expert in looking for answers in the knowledge base.",
    # memory=memory,
    # enable_session_summaries=True,
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=["Always look for answers in the knowledge base.", "If you don't find an answer, say 'No relevant information found'."],
    show_tool_calls=True,
    markdown=True
)

greeting_agent = Agent(
    name="Greeting Agent",
    description="You are an expert in conversational responses, acting like a human colleague.",
    # description="You are an expert in greeting people",
    # model=OpenRouter(id="gpt-4o"),
    model=Groq(id="llama-3.3-70b-versatile"),
    # model=Groq(id="gemma2-9b-it"),
    instructions=["Respond as if you are a human colleague and keep responses friendly and professional.",
                  "Deflect politely to personal questions.",],
    show_tool_calls=True,
    markdown=True
)

supervisor_team = Team(
    name="Supervisor Team",
    mode="route",
    members=[email_agent, knowledge_agent, greeting_agent],
    # model=OpenRouter(id="gpt-4o"),
    memory=memory,
    enable_session_summaries=True,
    model=Groq(id="llama-3.3-70b-versatile"),
    description="You are a supervisor who can analyze the query and route to the appropriate agent.",
    instructions=[
        "Route to the Greeting Agent for greetings.",
        "Route to the Email Agent only for sending emails.",
        "Route to Knowledge Agent for rest of the questions."
    ],
    show_tool_calls=True,
    markdown=True
)


async def on_turn(turn_context: TurnContext):
    activity = turn_context.activity

    # Handle user messages
    if activity.type == ActivityTypes.message:
        user_text = activity.text
        response_text = supervisor_team.run(user_text)
        response_text = response_text.content
        await turn_context.send_activity(MessageFactory.text(response_text))
        return

    # Handle new members joining
    if activity.type == ActivityTypes.conversation_update and activity.members_added:
        for member in activity.members_added:
            if member.id != activity.recipient.id:
                await turn_context.send_activity("Hello! How can I assist you today?")
                return


@app.get("/")
async def root():
    return {"message": "Teams Chatbot API is running"}


@app.post("/api/messages")
async def messages(request: Request):
    try:
        body = await request.json()
        
        activity = Activity().deserialize(body)

        auth_header = request.headers.get("Authorization", "")
        await adapter.process_activity(activity, auth_header, on_turn)

        return {}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)