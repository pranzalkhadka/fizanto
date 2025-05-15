from agno.agent import Agent, AgentKnowledge
from agno.models.groq import Groq
# from agno.models.anthropic import Claude
from agno.models.openrouter import OpenRouter
from agno.models.google import Gemini
from agno.team import Team
from agno.vectordb.lancedb import LanceDb
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.tools.file import FileTools
from agno.tools import tool
from weasyprint import HTML
from agno.tools import tool
import os


# claude_api_key = "api-key"

# GEMINI_API_KEY="api-key"

# openrouter_api_key = "api-key"

# GROQ_API_KEY = "api-key"


knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="tmp_app/lancedb",
        table_name="data_memory",
        embedder=FastEmbedEmbedder(id="BAAI/bge-small-en-v1.5")
    )
)

Introduction_agent = Agent(
    name="Introduction Agent",
    # model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=OpenRouter(id="gemini-2.0-flash", api_key=openrouter_api_key),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Introduction section of a Model Risk Management (MRM) Validation Report for a credit risk model, targeting at least 15 pages.",
    "Search the knowledge base for the model’s purpose, business context, and performance summary.",
    "Highlight the model’s role in loan approval decisions.",
],
    show_tool_calls=False,
    markdown=False
)

Overview_agent = Agent(
    name="Overview Agent",
    # model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=OpenRouter(id="gemini-2.0-flash", api_key=openrouter_api_key),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Model Overview section of a Model Risk Management (MRM) Validation Report for a credit risk model, targeting at least 15 pages.",
    "Search the knowledge base for the model’s design, purpose, and data sources.",
    "Include key features’ roles in predicting defaults.",
],
    show_tool_calls=False,
    markdown=False
)

Scope_agent = Agent(
    name="Scope Agent",
    # model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    # model=OpenRouter(id="gemini-2.0-flash", api_key=openrouter_api_key),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Validation Scope and Objectives section of a Model Risk Management (MRM) Validation Report for a credit risk model, targeting at least 15 pages.",
    "Search the knowledge base for validation goals and scope.",
],
    show_tool_calls=False,
    markdown=False
)

Methodology_agent = Agent(
    name="Methodology Agent",
    # model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=OpenRouter(id="gemini-2.0-flash", api_key=openrouter_api_key),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Methodology section of a Model Risk Management (MRM) Validation Report for a credit risk model, targeting at least 15 pages.",
    "Search the knowledge base for validation methods.",
],
    show_tool_calls=False,
    markdown=False
)

Recommendations_agent = Agent(
    name="Recommendations Agent",
    # model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=OpenRouter(id="gemini-2.0-flash", api_key=openrouter_api_key),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Recommendations section of a Model Risk Management (MRM) Validation Report for a credit risk model, targeting at least 15 pages.",
    "Search the knowledge base for suggested improvements and limitations.",
],
    show_tool_calls=False,
    markdown=False
)

Conclusion_agent = Agent(
    name="Conclusion Agent",
    # model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=OpenRouter(id="gemini-2.0-flash", api_key=openrouter_api_key),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Conclusion section of a Model Risk Management (MRM) Validation Report for a credit risk model, targeting at least 15 pages.",
    "Search the knowledge base for the model’s performance, limitations, and overall assessment.",
],
    show_tool_calls=False,
    markdown=False
)

Appendices_agent = Agent(
    name="Appendices Agent",
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY),
    # model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=OpenRouter(id="gemini-2.0-flash", api_key=openrouter_api_key),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a detailed Appendices section of a Model Risk Management (MRM) Validation Report, targeting at least 15 pages.",
        "Search the knowledge base for supplementary materials related to the validation.",
    ],
    show_tool_calls=False,
    markdown=False
)

# from markdown_pdf import MarkdownPdf, Section

# @tool(
#     name="markdown_to_pdf",
#     description="Convert a Markdown file to a PDF file",
#     show_result=False,
#     stop_after_tool_call=False,
#     cache_results=False
# )
# def markdown_to_pdf(input_file: str = "report.md", output_file: str = "report.pdf"):
#     try:
#         output_file: str = "report.pdf"

#         with open(input_file, "r") as f:
#             markdown_content = f.read()
        
#         # Create PDF
#         pdf = MarkdownPdf()
#         pdf.meta["title"] = "Model Risk Management Validation Report"
#         pdf.add_section(Section(markdown_content, toc=False))
#         pdf.save(output_file)
        
#         return f"PDF saved at {output_file}"
#     except Exception as e:
#         return f"Error converting Markdown to PDF: {str(e)}"



supervisor_team = Team(
    name="Supervisor Team",
    mode="coordinate",
    members=[
        Introduction_agent,
        Overview_agent,
        Scope_agent,
        Methodology_agent,
        Recommendations_agent,
        Conclusion_agent,
        Appendices_agent,
    ],
    # model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY),
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=OpenRouter(id="gemini-2.0-flash", api_key=openrouter_api_key),
    description="Coordinates the generation of a Model Risk Management (MRM) Validation Report.",
    tools=[FileTools()],
    # tools=[FileTools(base_dir=".", read_files=True, save_files=True, list_files=False)],
    instructions=[
    "When the query requests a Model Risk Management (MRM) Validation Report, follow these steps:",
    "1. Delegate tasks to Agents to generate content for each section:",
    "   - Ask Introduction Agent for the Introduction section.",
    "   - Ask Overview Agent for the Model Overview section.",
    "   - Ask Scope Agent for the Scope section.",
    "   - Ask Methodology Agent for the Methodology section.",
    "   - Ask Recommendations Agent for the Recommendations section.",
    "   - Ask Conclusion Agent for the Conclusion section.",
    "   - Ask Appendices Agent for the Appendices section.",
    "2. Save all the generated contents to a file.",
],
    show_tool_calls=True,
    markdown=True,
    enable_agentic_context=False,
    share_member_interactions=False,
    show_members_responses=True
)

supervisor_team.print_response("Generate a Model Risk Management Validation Report.")

# "2. Collect all the Markdown content from the Agents, combine it and save it to a file report.md.",
# "3. Convert 'report.md' to 'report.pdf' using markdown_to_pdf tool."
# "4. Return a message: 'MD file saved at report.md and and PDF file saved at report.pdf'."