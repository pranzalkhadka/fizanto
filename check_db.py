import lancedb
import json

DB_URI = "/home/pranjal/Downloads/fizanto/tmp/lancedb"
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

