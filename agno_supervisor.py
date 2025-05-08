from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openrouter import OpenRouter
from agno.models.google import Gemini
from agno.models.anthropic import Claude
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
    model=Groq(id="llama-3.3-70b-versatile"),
    # model=Groq(id="gemma2-9b-it"),
    instructions=["Respond as if you are a human colleague and keep responses friendly and professional.",
                  "Deflect politely to personal questions.",],
    show_tool_calls=True,
    markdown=True
)

import subprocess


@tool(
    name="run_analysis",
    description="Run analysis to retrieve answer for the user query",
    show_result=True,
    stop_after_tool_call=True,
    cache_results=False
)
def run_analysis(user_prompt: str) -> str:
    """
    Use this function to retreive answer for the user query.
    """
    try:
        docker_command = [
            "docker", "run", "--rm",
            "--add-host=host.docker.internal:host-gateway",
            "-v", "/home/pranjal/Downloads/fizanto/attachments:/app/attachments",
            "-v", "/home/pranjal/Downloads/fizanto/.env:/app/.env",
            "-e", f"ANALYSIS_PROMPT={user_prompt}",
            "analysis-service"
        ]
        result = subprocess.run(
            docker_command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout or "No analysis output generated."
    except subprocess.CalledProcessError as e:
        return f"Failed to run Docker analysis: {e.stderr}"
    except Exception as e:
        return f"Error running Docker analysis: {str(e)}"

    
# knowledge_agent = Agent(
#     name="Knowledge Agent",
#     model=Groq(id="llama-3.3-70b-versatile"),
#     tools=[run_analysis],
#     instructions=["Call the run_analysis tool to get answer for the user's question",],
#     show_tool_calls=True,
#     markdown=True
# )


knowledge_agent = Agent(
    name="Knowledge Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Claude(id="claude-3-7-sonnet-20250219", api_key="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"),
    tools=[run_analysis],
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=["First search the knowledge base for answer.", 
                  "If no relevant answer is found in the knowledge base, call the run_analysis tool to get the answer"],
    show_tool_calls=True,
    markdown=True
)


# knowledge_agent = Agent(
#     name="Knowledge Agent",
#     # model=Groq(id="llama-3.3-70b-versatile"),
#     # model=MistralChat(id="mistral-large-latest"),
#     # model=Gemini(id="gemini-2.0-flash"),
#     # model=OpenRouter(id="gpt-4o"),
#     model=Claude(id="claude-3-7-sonnet-20250219", api_key="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"),
#     description="You are an expert in looking for answers in the knowledge base.",
#     # memory=memory,
#     # enable_session_summaries=True,
#     knowledge=knowledge_base,
#     search_knowledge=True,
#     instructions=["Always look for answers in the knowledge base.", "If you don't find an answer, say 'No relevant information found'."],
#     show_tool_calls=True,
#     markdown=True
# )


supervisor_team = Team(
    name="Supervisor Team",
    mode="route",
    members=[email_agent, knowledge_agent, greeting_agent],
    # model=OpenRouter(id="gpt-4o"),
    memory=memory,
    enable_session_summaries=True,
    # model=Groq(id="llama-3.3-70b-versatile"),
    # model=MistralChat(id="mistral-large-latest"),
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyBXiMNmOVmrCnOCP-sjGcaPnL1bTfzDI2Y"),
    description="You are a supervisor who can analyze the query and route to the appropriate agent.",
    instructions=[
        "Route to the Greeting Agent for greetings.",
        "Route to the Email Agent only for sending emails. Not for email inquiries.",
        "Route to Knowledge Agent for rest of the questions."
    ],
    show_tool_calls=True,
    markdown=True
)


# supervisor_team.print_response("I hope you got my email with regards to the Lending Club Credit Risk Model. Can you confirm that?", user_id=user_id, session_id=session_id)
# supervisor_team.print_response("What are the core assumptions of the Lending Club loan default prediction model?", user_id=user_id, session_id=session_id)
# supervisor_team.print_response("What are the risk factors associated with the Lending Club loan default prediction model?", user_id=user_id, session_id=session_id)
# supervisor_team.print_response("What input features are used in the Lending Club credit risk model?", user_id=user_id, session_id=session_id)
# supervisor_team.print_response("Could you show me the validation performance metrics? It'd be helpful to see some visualizations of the model's performance.", user_id=user_id, session_id=session_id)
supervisor_team.print_response("What is the average annual income?", user_id=user_id, session_id=session_id)
