from agno.agent import Agent, AgentKnowledge
from agno.models.groq import Groq
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.team import Team
from agno.vectordb.lancedb import LanceDb
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.tools.file import FileTools
from agno.tools import tool
from weasyprint import HTML
from agno.tools import tool
import os

claude_api_key = "api-key"

# groq_api_key = "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"

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# GEMINI_API_KEY="AIzaSyBXiMNmOVmrCnOCP-sjGcaPnL1bTfzDI2Y"


knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="tmp_app/lancedb",
        table_name="data_memory",
        embedder=FastEmbedEmbedder(id="BAAI/bge-small-en-v1.5")
    )
)

Introduction_agent = Agent(
    name="Introduction Agent",
    model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=groq_api_key),
    # model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Introduction section of a Model Risk Management (MRM) Validation Report for a credit risk model.",
    "Search the knowledge base for the model’s purpose, business context, and performance summary.",
    "Highlight the model’s role in loan approval decisions.",
    "Return the content in a Markdown format."
],
    show_tool_calls=False,
    markdown=False
)

Overview_agent = Agent(
    name="Overview Agent",
    model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=groq_api_key),
    # model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Model Overview section of a Model Risk Management (MRM) Validation Report for a credit risk model.",
    "Search the knowledge base for the model’s design, purpose, and data sources.",
    "Include key features’ roles in predicting defaults.",
    "Return the content in Markdown format."
],
    show_tool_calls=False,
    markdown=False
)

Scope_agent = Agent(
    name="Scope Agent",
    model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=Groq(id="llama-3.1-8b-instant", api_key=groq_api_key),
    # model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Validation Scope and Objectives section of a Model Risk Management (MRM) Validation Report for a credit risk model.",
    "Search the knowledge base for validation goals and scope.",
    "Return the content in Markdown format."
],
    show_tool_calls=False,
    markdown=False
)

Methodology_agent = Agent(
    name="Methodology Agent",
    model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=groq_api_key),
    # model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Validation Methodology section of a Model Risk Management (MRM) Validation Report for a credit risk model.",
    "Search the knowledge base for validation methods.",
    "Return the content in Markdown format."
],
    show_tool_calls=False,
    markdown=False
)

Recommendations_agent = Agent(
    name="Recommendations Agent",
    model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=groq_api_key),
    # model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Recommendations section of a Model Risk Management (MRM) Validation Report for a credit risk model.",
    "Search the knowledge base for suggested improvements and limitations.",
    "Return the content in Markdown format."
],
    show_tool_calls=False,
    markdown=False
)

Conclusion_agent = Agent(
    name="Conclusion Agent",
    model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
    # model=Groq(id="llama-3.1-8b-instant", api_key=groq_api_key),
    # model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
    # model=Groq(id="gemma2-9b-it"),
    # model=OpenRouter(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
    "Generate a highly detailed Conclusion section of a Model Risk Management (MRM) Validation Report for a credit risk model.",
    "Search the knowledge base for the model’s performance (e.g., AUC-ROC, recall), limitations, and overall assessment.",
    "Return the content in Markdown format."
],
    show_tool_calls=False,
    markdown=False
)

# Appendices_agent = Agent(
#     name="Appendices Agent",
#     # model=Groq(id="llama-3.3-70b-versatile"),
#     # model=Groq(id="gemma2-9b-it"),
#     model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
#     # model=OpenRouter(id="gpt-4o"),
#     knowledge=knowledge_base,
#     search_knowledge=True,
#     # instructions=[
#     #     "Generate a highly detailed Appendices section for a Model Risk Management (MRM) Validation Report for a credit risk model, contributing to a 100+ page report.",
#     #     "Search the knowledge base for supplementary materials, including model documentation, validation results, feature importance, data quality logs, governance records, stress testing, fairness analyses, and monitoring plans.",
#     #     "Produce multiple subsections in Markdown format, such as:",
#     #     "  - Model Documentation: LightGBM methodology, hyperparameters, tuning logs.",
#     #     "  - Validation Results: K-fold CV, backtesting, fairness metrics (tables).",
#     #     "  - Feature Importance: Top 20 features with SHAP values, descriptions.",
#     #     "  - Data Quality Logs: Missing value imputation, preprocessing details.",
#     #     "  - Governance Records: MRM committee approvals, independent reviews.",
#     #     "  - Stress Testing: Scenario analyses (e.g., recession, rate hikes).",
#     #     "  - Fairness Analyses: Bias assessments, mitigation steps.",
#     #     "  - Monitoring Plans: Drift detection, retraining triggers.",
#     #     "Include at least 10 Markdown tables (e.g., metrics, features, preprocessing steps).",
#     #     "Aim for 50+ pages of content, ensuring SR 11-7 traceability."
#     # ],
#     instructions=[
#         "Generate a detailed Appendices section of a Model Risk Management (MRM) Validation Report.",
#         "Search the knowledge base for supplementary materials related to the validation.",
#         "Return only text in Markdown format.",
#     ],
#     show_tool_calls=False,
#     markdown=False
# )


@tool(
    name="html_to_pdf",
    description="Convert an HTML file to a PDF file",
    show_result=False,
    stop_after_tool_call=False,
    cache_results=False
)
def html_to_pdf(input_file: str = "report.html", output_file: str = "report.pdf") -> str:
    """
    Convert an HTML file to a PDF file.
    
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
    ],
    # model=Groq(id="llama-3.3-70b-versatile"),
    # model=Gemini(id="gemini-2.0-flash"),
    model=Claude(id="claude-3-7-sonnet-20250219", api_key=claude_api_key),
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
    "3. Collect the Markdown content into a dictionary with keys: introduction_text, model_overview_text, validation_scope_text, methodology_text, recommendations_text, conclusion_text.",
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