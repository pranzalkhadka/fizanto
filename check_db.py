import lancedb
import json

DB_URI = "tmp/lancedb"
TABLE_NAME = "email_memory"

def check_stored_data():
    db = lancedb.connect(DB_URI)
    
    if TABLE_NAME not in db.table_names():
        print(f"No table '{TABLE_NAME}' found in {DB_URI}.")
        return
    
    table = db.open_table(TABLE_NAME)
    
    all_data = table.search().limit(10).to_pandas()
    
    if all_data.empty:
        print("No data stored in the knowledge base.")
    else:
        print("Stored data in LanceDb:")
        for index, row in all_data.iterrows():
            payload = json.loads(row['payload'])
            content = payload.get('content', 'No content found')
            print(f"Entry {index + 1}: {content}")

if __name__ == "__main__":
    check_stored_data()





# from agno.embedder.fastembed import FastEmbedEmbedder
# from agno.agent import AgentKnowledge
# from agno.vectordb.lancedb import LanceDb


# query = "Did you receive the email about Lending Club Risk Management?"


# knowledge_base = AgentKnowledge(
#     vector_db=LanceDb(
#         uri="tmp/lancedb",
#         table_name="email_memory",
#         embedder=FastEmbedEmbedder(id="BAAI/bge-small-en-v1.5")
#     )
# )

# results = knowledge_base.search(query)
# for result in results:
#     print(result.content)


# import sqlite3
# from agno.memory.v2.memory import Memory
# print("Memory module imported successfully.")