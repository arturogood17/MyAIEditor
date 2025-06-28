from dotenv import load_dotenv
from google import genai
from google.genai import types
from available_functions import available_functions, calling_function
from system_prompt  import SYSTEMP_PROMPT
import os, sys

def main():
    load_dotenv()

    if len(sys.argv) <= 1:
        print("No prompt was provided.")
        print("Usage: python main.py 'prompt'.")
        sys.exit(1)


    verbose = "--verbose" in sys.argv[1:]
    prompt = " ".join(sys.argv[1:-1])
    if verbose:
        print(f"User prompt:", prompt)
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    generate_content(client, messages, verbose)



def generate_content(client, messages, verbose):
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              config=types.GenerateContentConfig(system_instruction=SYSTEMP_PROMPT, tools=[available_functions]),
                                              contents= messages,
                                              )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.function_calls:
        return ("Response:", response.text)
    
    functions_called_so_far = []
    for function in response.function_calls:
        function_called = calling_function(function, verbose)
        if (
            not function_called.parts
            or not function_called.parts[0].function_response.response):
            raise Exception("empty function call result")
        if verbose:
            print(f'-> {function_called.parts[0].function_response.response}')
        
        functions_called_so_far.append(function_called.parts[0])
        
        if not functions_called_so_far:
            raise Exception("No function response was generated.")
        

if __name__ == "__main__":
    main()
