from dotenv import load_dotenv
from google import genai
import os

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
