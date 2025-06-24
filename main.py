from dotenv import load_dotenv
from google import genai
from google.genai import types
import os, sys

def main():
    load_dotenv()

    if len(sys.argv) <= 1:
        print("No prompt was provided.")
        sys.exit(1)
    
    verbose = "--verbose" in sys.argv[1:]
    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents= messages)
    if verbose:
        print("User prompt:", prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    print(response.text)

if __name__ == "__main__":
    main()
