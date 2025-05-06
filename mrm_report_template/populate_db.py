from agno.vectordb.lancedb import LanceDb
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.agent import Agent, AgentKnowledge
import os

os.makedirs("tmp_app/lancedb", exist_ok=True)

knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="tmp_app/lancedb",
        table_name="data_memory",
        embedder=FastEmbedEmbedder(id="BAAI/bge-small-en-v1.5")
    )
)

analysis_data = [
    "The financial forecasting model uses time-series analysis to predict revenue trends based on historical data and market indicators, validated in 2024.",
    "The model aims to provide accurate revenue projections for strategic planning.",
    "The validation process ensures compliance with regulatory standards and organizational policies.",
    "Validation scope includes assessing the model's conceptual soundness and performance metrics.",
    "Methodology involves qualitative reviews, such as documentation analysis, and quantitative tests, like stress testing.",
    "Recommendations include improving data preprocessing and updating documentation.",
    "The model is fit for purpose but requires minor improvements for reliability.",
    "Appendices include model documentation and validation test results."
]

for text in analysis_data:
    knowledge_base.load_text(text)

print("Knowledge base populated with sample data.")