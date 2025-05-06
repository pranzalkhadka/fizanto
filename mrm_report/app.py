from agno.agent import Agent, AgentKnowledge
from agno.models.groq import Groq
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

knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="tmp_app/lancedb",
        table_name="data_memory",
        embedder=FastEmbedEmbedder(id="BAAI/bge-small-en-v1.5")
    )
)

Introduction_agent = Agent(
    name="Introduction Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Introduction section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for context about the financial forecasting model and its validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=False,
    markdown=False
)

Overview_agent = Agent(
    name="Overview Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Model Overview section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for details about the financial forecasting model's design and purpose.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=False,
    markdown=False
)

Scope_agent = Agent(
    name="Scope Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Validation Scope and Objectives section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for the scope of the model's validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=False,
    markdown=False
)

Methodology_agent = Agent(
    name="Methodology Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Validation Methodology section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for methods used in the model's validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=False,
    markdown=False
)

Recommendations_agent = Agent(
    name="Recommendations Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Recommendations section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for suggested improvements from the validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=False,
    markdown=False
)

Conclusion_agent = Agent(
    name="Conclusion Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Conclusion section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for the overall assessment of the model's validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=False,
    markdown=False
)

Appendices_agent = Agent(
    name="Appendices Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Appendices section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for supplementary materials related to the validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=False,
    markdown=False
)


@tool(
    name="html_to_pdf",
    description="Convert an HTML file to a PDF file",
    show_result=False,
    stop_after_tool_call=False,
    cache_results=False
)
def html_to_pdf(input_file: str = "report.html", output_file: str = "report.pdf") -> str:
    """
    Convert an HTML file to a PDF file using WeasyPrint.
    
    Args:
        input_file (str): Path to the input HTML file (default: 'report.html').
        output_file (str): Path to the output PDF file (default: 'report.pdf').
    
    Returns:
        str: Confirmation message indicating the PDF was saved.
    """
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file {input_file} not found")
        HTML(input_file).write_pdf(output_file)
        return f"PDF saved at {output_file}"
    except Exception as e:
        return f"Error converting HTML to PDF: {str(e)}"



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
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=Gemini(id="gemini-2.0-flash"),
    # model=OpenRouter(id="gpt-4o"),
    description="Coordinates the generation of a Model Risk Management (MRM) Validation Report.",
    tools=[FileTools(), html_to_pdf],
    # tools=[FileTools(base_dir=".", read_files=True, save_files=True, list_files=False)],
    instructions=[
    "When the query requests a Model Risk Management (MRM) Validation Report, follow these steps:",
    "1. Use FileTools.read_file('template.html') to load the HTML template.",
    "2. Delegate tasks to content Agents to generate Markdown paragraphs for each section:",
    "   - Ask Introduction Agent for the Introduction section.",
    "   - Ask Overview Agent for the Model Overview section.",
    "   - Ask Scope Agent for the Validation Scope section.",
    "   - Ask Methodology Agent for the Validation Methodology section.",
    "   - Ask Recommendations Agent for the Recommendations section.",
    "   - Ask Conclusion Agent for the Conclusion section.",
    "   - Ask Appendices Agent for the Appendices section.",
    "3. Collect the Markdown content into a dictionary with keys: introduction_text, model_overview_text, validation_scope_text, methodology_text, recommendations_text, conclusion_text, appendices_text.",
    "4. Use that dictionary to fill the placeholders in the HTML template.",
    "5. Save the HTML file at report.html."
    "6. Convert 'report.html' to 'report.pdf' using html_to_pdf tool."
    "7. Return a message: 'HTML saved at report.html and and PDF saved at report.pdf'."
],
    show_tool_calls=False,
    markdown=False,
    enable_agentic_context=False,
    share_member_interactions=False,
    show_members_responses=True
)


supervisor_team.print_response("Generate a Model Risk Management Validation Report.")