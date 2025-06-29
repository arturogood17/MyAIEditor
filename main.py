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
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    prompt = " ".join(args)
    if verbose:
        print(f"User prompt:", prompt)
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    i = 0
    while True:
        i += 1
        if i > 20:
            print("Max iteretions reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
            else:
                continue
        except Exception as e:
            print(f"Error trying to generate content: {e}")
            


def generate_content(client, messages, verbose):
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages,
                                              config=types.GenerateContentConfig(system_instruction=SYSTEMP_PROMPT,
                                                                                 tools=[available_functions]),
                                              )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return (response.text)
            
    function_responses = []
    for function in response.function_calls:
        function_called = calling_function(function, verbose)
        if (
            not function_called.parts
            or not function_called.parts[0].function_response.response):
            raise Exception("empty function call result")
        if verbose:
            print(f'-> {function_called.parts[0].function_response.response}')
        
        function_responses.append(function_called.parts[0])

    if not function_responses:
        raise Exception("no function responses generated.")
    
    messages.append(types.Content(role="tool", parts=function_responses))
        

if __name__ == "__main__":
    main()
