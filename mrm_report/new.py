# import os
# import json
# import logging
# from agno.agent import Agent
# from agno.models.google import Gemini

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Configuration
# GEMINI_API_KEY = "AIzaSyAhwnAFLK3RPzqh8WALRigSQxYArgHmrus"
# REPORT_DIR = "/home/pranjal/Downloads/fizanto/mrm_report"
# JSON_PATH = os.path.join(REPORT_DIR, "reportData33.json")
# os.makedirs(REPORT_DIR, exist_ok=True)

# # Agent
# content_agent = Agent(
#     name="Content Agent",
#     model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_API_KEY),
#     instructions=[
#         "Generate content for a Model Risk Management (MRM) Validation Report for a credit risk model.",
#         "Produce one paragraph (3 to 5 sentences) for each of the following sections, and return as a JSON object with keys matching the template placeholders.",
#         "Use general knowledge to create realistic content. Avoid placeholders like '[Value]'.",
#         "Sections:",
#         "  - introduction_text: Introduce the credit risk model and its purpose.",
#         "  - model_overview_text: Describe the model's structure or key features.",
#         "  - validation_scope_text: Outline the scope of the validation process.",
#         "  - methodology_text: Explain the validation methodology briefly.",
#         "  - recommendations_text: Provide a key recommendation for model improvement.",
#         "  - conclusion_text: Summarize the validation findings.",
#         "  - appendices_text: Describe what the appendices contain.",
#         "Return a JSON object like: {\"introduction_text\": \"The credit risk model...\", \"model_overview_text\": \"The model uses...\", ...}.",
#     ],
#     show_tool_calls=False
# )

# def generate_json():
#     """Generate JSON content using the agent and save to reportData.json."""
#     try:
#         # Generate content
#         logger.info("Generating content with agent")
#         response = content_agent.run("Generate content for the MRM Validation Report.")
        
#         # Extract JSON string from RunResponse
#         if not hasattr(response, 'content'):
#             raise ValueError("Response lacks 'content' attribute")
#         json_string = response.content
#         logger.info("Extracted JSON string (first 100 chars): %s", json_string[:100])

#         # Parse JSON response
#         try:
#             data = json.loads(json_string)
#         except json.JSONDecodeError as e:
#             logger.error("Invalid JSON response: %s", str(e))
#             raise

#         # Validate required keys
#         required_keys = [
#             "introduction_text", "model_overview_text", "validation_scope_text",
#             "methodology_text", "recommendations_text", "conclusion_text", "appendices_text"
#         ]
#         for key in required_keys:
#             if key not in data:
#                 logger.error("Missing key in JSON: %s", key)
#                 raise KeyError(f"Missing key: {key}")

#         # Save JSON
#         with open(JSON_PATH, 'w', encoding='utf-8') as f:
#             json.dump(data, f, indent=2)
#         logger.info("Saved %s (%d bytes)", JSON_PATH, os.path.getsize(JSON_PATH))

#         return f"JSON saved at {JSON_PATH}"
#     except Exception as e:
#         logger.error("Error generating JSON: %s", str(e))
#         return f"Error generating JSON: {str(e)}"

# if __name__ == "__main__":
#     print(generate_json())


# import google.generativeai as genai

# genai.configure(api_key="AIzaSyAhwnAFLK3RPzqh8WALRigSQxYArgHmrus")  

# model = genai.GenerativeModel('gemini-1.5-flash')  

# prompt = """
# Generate content for various sections of a Model Risk Management (MRM) Validation Report for a credit risk model. 
# The sections are: introduction, model_overview, validation_scope, methodology, recommendations, conclusion, appendices. 
# Each section should be a paragraph (3 to 5 sentences) and return as a JSON object with keys matching the sections. 
# """
# response = model.generate_content(prompt)

# print(response.text)


import google.generativeai as genai
import json
import os

# Configure Gemini
genai.configure(api_key="AIzaSyAhwnAFLK3RPzqh8WALRigSQxYArgHmrus")
model = genai.GenerativeModel('gemini-1.5-flash')

# Define output path
REPORT_DIR = "/home/pranjal/Downloads/fizanto/mrm_report"
JSON_PATH = os.path.join(REPORT_DIR, "reportData22.json")
os.makedirs(REPORT_DIR, exist_ok=True)

# Prompt
prompt = """
Generate content for various sections of a Model Risk Management (MRM) Validation Report for a credit risk model. 
The sections are: introduction, model_overview, validation_scope, methodology, recommendations, conclusion, appendices. 
Each section should be a paragraph (3 to 5 sentences). 
Return the content as a valid JSON object with keys matching the sections, like this:
{
  "introduction": "Paragraph text here...",
  "model_overview": "Paragraph text here...",
  "validation_scope": "Paragraph text here...",
  "methodology": "Paragraph text here...",
  "recommendations": "Paragraph text here...",
  "conclusion": "Paragraph text here...",
  "appendices": "Paragraph text here..."
}
Ensure the response is a properly formatted JSON string, enclosed in ```json\n...\n``` for clarity.
"""

# Generate content
try:
    response = model.generate_content(prompt)
except Exception as e:
    print(f"Error generating content: {str(e)}")
    exit(1)

# Debug: Print raw response
print("Raw response text:", response.text)

# Parse JSON string
try:
    json_string = response.text
    # Extract JSON from ```json\n...\n``` if present
    if json_string.startswith("```json\n") and json_string.endswith("\n```"):
        json_string = json_string[7:-3].strip()  # Remove ```json\n and \n```
    elif json_string.startswith("```"):
        json_string = json_string[3:-3].strip()  # Handle plain ``` code blocks
    else:
        json_string = json_string.strip()  # Remove leading/trailing whitespace
    if not json_string:
        raise ValueError("JSON string is empty after processing")
    data = json.loads(json_string)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {str(e)}")
    print(f"Processed JSON string: {json_string!r}")
    print("Response is not valid JSON. Check the raw response and processed string above.")
    exit(1)
except ValueError as e:
    print(f"Error processing JSON: {str(e)}")
    exit(1)

# Save to JSON file
try:
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"JSON saved at {JSON_PATH}")
except Exception as e:
    print(f"Error saving JSON: {str(e)}")