# main.py

from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-1219")
response = model.generate_content("Explain how AI works")
for chunk in response:
    print(chunk.text)
    print("_" * 80)

