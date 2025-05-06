from agno.agent import Agent, AgentKnowledge
from agno.models.groq import Groq
from agno.team import Team
from agno.vectordb.lancedb import LanceDb
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.tools.file import FileTools
import json
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
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Introduction section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for context about the financial forecasting model and its validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=True,
    markdown=True
)

Overview_agent = Agent(
    name="Overview Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Model Overview section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for details about the financial forecasting model's design and purpose.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=True,
    markdown=True
)

Scope_agent = Agent(
    name="Scope Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Validation Scope and Objectives section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for the scope of the model's validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=True,
    markdown=True
)

Methodology_agent = Agent(
    name="Methodology Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Validation Methodology section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for methods used in the model's validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=True,
    markdown=True
)

Recommendations_agent = Agent(
    name="Recommendations Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Recommendations section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for suggested improvements from the validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=True,
    markdown=True
)

Conclusion_agent = Agent(
    name="Conclusion Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Conclusion section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for the overall assessment of the model's validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=True,
    markdown=True
)

Appendices_agent = Agent(
    name="Appendices Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "Generate a single paragraph for the Appendices section of a Model Risk Management (MRM) Validation Report.",
        "Search the knowledge base for supplementary materials related to the validation.",
        "Return the paragraph in Markdown format.",
    ],
    show_tool_calls=True,
    markdown=True
)



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
    model=Groq(id="llama-3.3-70b-versatile"),
    description="Coordinates the generation of a Model Risk Management (MRM) Validation Report.",
    tools=[FileTools()],
    instructions=[
        "When the query requests a Model Risk Management (MRM) Validation Report, follow these steps:",
        "1. Delegate tasks to each Agents to generate content for each section:",
        "   - Ask Introduction Agent for the Introduction section.",
        "   - Ask Overview Agent for the Model Overview section.",
        "   - Ask Scope Agent for the Validation Scope section.",
        "   - Ask Methodology Agent for the Validation Methodology section.",
        "   - Ask Recommendations Agent for the Recommendations section.",
        "   - Ask Conclusion Agent for the Conclusion section.",
        "   - Ask Appendices Agent for the Appendices section.",
        "2. Collect the content from each Agent. Save the answer to a file."
    ],
    show_tool_calls=True,
    markdown=True,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True
)


supervisor_team.print_response("Generate a Model Risk Management Validation Report.")