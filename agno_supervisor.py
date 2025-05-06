from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openrouter import OpenRouter
from agno.team import Team
import os
from agno.vectordb.lancedb import LanceDb
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.agent import Agent, AgentKnowledge
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from agno.tools import tool
import re
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory

memory_db = SqliteMemoryDb(table_name="memory", db_file="/home/pranjal/Downloads/fizanto/memoryy/memory_session.db")
memory = Memory(db=memory_db)

user_id = "jon_hamm@example.com"
session_id = "1001"

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="email_memory",
        embedder=FastEmbedEmbedder(id="BAAI/bge-small-en-v1.5")
    )
)


def extract_email_metadata():

    session_summary = memory.get_session_summary(
    user_id=user_id, session_id=session_id)

    # query = "Email about Lending Club Risk Management"

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

# try:
#     # supervisor_team.print_response("What is the file lending_club_raw_data about?")
#     supervisor_team.print_response("Did you receive my email about Lending Club Risk Management artifacts?")
#     # supervisor_team.print_response("What is in the email attachment?")
#     # supervisor_team.print_response("What is the file data_sample_metadata about?")
#     # supervisor_team.print_response("Hello, how are you?", stream=True)
#     # supervisor_team.print_response("What is the file medicine about?")
#     # supervisor_team.print_response("What are lending_club_raw_data.csv and data_sample_metadata.md about?")
#     # supervisor_team.print_response("What time is it?")
#     # supervisor_team.print_response("")
#     # supervisor_team.print_response("Send me an email")
#     print(knowledge_agent.memory)
#     pprint([m.model_dump(include={"role", "content"}) for m in knowledge_agent.memory.messages])
# except Exception as e:
#     print(f"Error: {e}")



# supervisor_team.print_response("Did you receive my email about Lending Club Risk Management artifacts?", user_id=user_id, session_id=session_id)
# supervisor_team.print_response("What is the file data_sample_metadata about?", session_id=session_id)
# supervisor_team.print_response("What is the file lending_club_raw_data about?", session_id=session_id)
# supervisor_team.print_response("Send me an email", user_id=user_id, session_id=session_id)
supervisor_team.print_response("Can you give summary of the data analysis?", user_id=user_id, session_id=session_id)

# session_summary = memory.get_session_summary(
#     user_id=user_id, session_id=session_id)
