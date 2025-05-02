from dotenv import load_dotenv
import os
import pandas as pd
from e2b_code_interpreter import Sandbox
from groq import Groq

load_dotenv()
E2B_API_KEY = os.getenv("E2B_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def get_csv_metadata(file_path: str) -> dict:
    """Extract metadata from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        metadata = {
            "columns": list(df.columns),
            "shape": df.shape
        }
        return metadata
    except Exception as e:
        raise Exception(f"Failed to read CSV: {e}")

def generate_human_readable_summary(metadata: dict, analysis_output: str) -> str:
    """Convert df.describe() output to a human-readable summary using Groq."""
    system_prompt = "You are a helpful assistant that summarizes data analysis results in plain English."
    user_prompt = f"""
    Given the following CSV metadata and raw analysis output from df.describe(), create a concise, human-readable summary of the key insights. Avoid technical jargon, code, or raw numbers. Focus on what the data tells us about the customers.

    Metadata:
    - Columns: {metadata['columns']}
    - Shape: {metadata['shape']}

    Raw Analysis Output:
    {analysis_output}

    Example Summary:
    The dataset includes information about bank customers. On average, customers earn a moderate income, with most being middle-aged. Credit card spending varies widely, and mortgages are common among a subset of customers.

    Return only the summary text.
    """
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    csv_path = "/home/pranjal/Downloads/fizanto/banlk_loan.csv"
    
    try:
        metadata = get_csv_metadata(csv_path)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    analysis_code = """
import pandas as pd
try:
    df = pd.read_csv('/home/user/banlk_loan.csv')
    print(df.describe().to_string())
except Exception as e:
    print(f"Error: {e}")
"""
    
    try:
        with Sandbox(api_key=E2B_API_KEY) as sbx:
            with open(csv_path, "rb") as f:
                sbx.files.write("/home/user/banlk_loan.csv", f)
            print("CSV uploaded to: /home/user/banlk_loan.csv")
            
            install_execution = sbx.run_code("!pip install pandas")
            if install_execution.logs.stderr:
                print("Package installation errors:", install_execution.logs.stderr)
                return
            
            execution = sbx.run_code(analysis_code)
            
            if execution.logs.stderr:
                print("Execution Errors:", execution.logs.stderr)
                return
            
            analysis_output = "\n".join(execution.logs.stdout)
            
            summary = generate_human_readable_summary(metadata, analysis_output)
            print("\n=== Analysis Summary ===")
            print(summary)
                
    except Exception as e:
        print(f"Sandbox error: {e}")

if __name__ == "__main__":
    main()