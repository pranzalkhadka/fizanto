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
# from agno.models.google import Gemini


load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
APP_ID = os.getenv('APP_ID')
APP_PASSWORD = os.getenv('APP_PASSWORD')

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

    results = knowledge_base.search(session_summary.summary)

    content = results[0].content

    sender_match = re.search(r"Received an email from (.+?) <(.+?)>", content)
    sender_name = sender_match.group(1) if sender_match else None
    recipient = sender_match.group(2) if sender_match else None

    subject_match = re.search(r"about (.+?) at", content)
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
    # description="Your only responsibility is sending emails.",
    # model=OpenRouter(id="gpt-4o"),
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[send_email],
    instructions=["Call the send_email tool to send an email"],
    show_tool_calls=True,
    markdown=True
)

greeting_agent = Agent(
    name="Greeting Agent",
    description="You are an expert in conversational responses, acting like a human colleague.",
    # description="You are an expert in greeting people",
    # model=OpenRouter(id="gpt-4o"),
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Groq(id="gemma2-9b-it"),
    instructions=["Respond as if you are a human colleague and keep responses friendly and professional.",
                  "Deflect politely to personal questions.",],
    show_tool_calls=True,
    markdown=True
)

import docker
from docker.errors import DockerException, ImageNotFound, APIError

@tool(
    name="run_analysis",
    description="Run analysis to retrieve answer for the user query",
    show_result=True,
    stop_after_tool_call=True,
    cache_results=False
)
def run_analysis(user_prompt: str) -> str:
    """
    Use this function to retrieve answer for the user query.
    """
    try:
        # Initialize Docker client
        client = docker.from_env()

        # Image name (use registry-hosted image for portability, e.g., Docker Hub)
        image_name = "pranjalkhadka/fizanto:analysis-service"  # Replace with your registry path

        # Pull the image if not already present
        try:
            client.images.get(image_name)
        except ImageNotFound:
            client.images.pull(image_name)

        # Run the container
        container = client.containers.run(
            image=image_name,
            command=None,  # Use the default command defined in the Dockerfile
            volumes={
                "/home/pranjal/Downloads/fizanto/attachments": {"bind": "/app/attachments", "mode": "rw"},
                "/home/pranjal/Downloads/fizanto/.env": {"bind": "/app/.env", "mode": "ro"}
            },
            environment=[f"ANALYSIS_PROMPT={user_prompt}"],
            remove=True,  # Equivalent to --rm
            detach=False  # Wait for the container to finish
        )

        # Container output is returned as bytes; decode to string
        output = container.decode("utf-8") if container else "No analysis output generated."
        return output

    except ImageNotFound:
        return f"Failed to find Docker image: {image_name}"
    except APIError as e:
        return f"Failed to run Docker analysis: {str(e)}"
    except DockerException as e:
        return f"Error running Docker analysis: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@tool(
    name="retrieve_filepath",
    description="Retrieve file path of the visualization",
    show_result=True,
    stop_after_tool_call=True,
    cache_results=False
)
def retrieve_filepath(user_prompt: str) -> str:
    """
    Use this function to retrieve file path of the visualization.
    """
    try:
        # Initialize Docker client
        client = docker.from_env()

        # Image name (use registry-hosted image for portability, e.g., Docker Hub)
        image_name = "pranjalkhadka/fizanto:vis-service"  # Replace with your registry path

        # Pull the image if not already present
        try:
            client.images.get(image_name)
        except ImageNotFound:
            client.images.pull(image_name)

        # Run the container
        container = client.containers.run(
            image=image_name,
            command=None,  # Use the default command defined in the Dockerfile
            volumes={
                "/home/pranjal/Downloads/fizanto/attachments": {"bind": "/app/attachments", "mode": "rw"},
                "/home/pranjal/Downloads/fizanto/output": {"bind": "/app/output", "mode": "rw"},
                "/home/pranjal/Downloads/fizanto/.env": {"bind": "/app/.env", "mode": "ro"}
            },
            environment=[f"VISUALIZATION_PROMPT={user_prompt}"],
            remove=True,  # Equivalent to --rm
            detach=False  # Wait for the container to finish
        )

        # Container output is returned as bytes; decode to string
        output = container.decode("utf-8") if container else "No visualizations generated."
        return output

    except ImageNotFound:
        return f"Failed to find Docker image: {image_name}"
    except APIError as e:
        return f"Failed to run Docker visualization: {str(e)}"
    except DockerException as e:
        return f"Error running Docker visualization: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


knowledge_agent = Agent(
    name="Knowledge Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    # model=Claude(id="claude-3-7-sonnet-20250219", api_key="claude_api_key"),
    tools=[run_analysis, retrieve_filepath],
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=["If the query is about creating plot, call the retrieve_filepath tool to get filepath of the plot.",
                  "If the query is about analysis, first search the knowledge base for relevant answer.", 
                  "If no relevant answer is found in the knowledge base, call the run_analysis tool to get the answer.",
                  ],
    show_tool_calls=True,
    markdown=True
)


supervisor_team = Team(
    name="Supervisor Team",
    mode="route",
    members=[email_agent, knowledge_agent, greeting_agent],
    memory=memory,
    enable_session_summaries=True,
    # model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    model=Groq(id="llama-3.3-70b-versatile"),
    description="You are a supervisor who can analyze the query and route to the appropriate agent.",
    instructions=[
        "Route to the Greeting Agent for greetings.",
        "Route to the Email Agent only for sending emails. Not for email inquiries.",
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