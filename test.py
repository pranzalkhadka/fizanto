# import pandas as pd


# d = pd.read_csv('banlk_loan.csv')
# print(d.head())



import google.generativeai as genai

genai.configure(api_key="key")  

model = genai.GenerativeModel('gemini-1.5-flash')  

prompt = "What is an LLM?"
response = model.generate_content(prompt)

print(response.text)