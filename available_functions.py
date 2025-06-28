from google.genai import types
from functions.get_files import get_files_info, schema_get_files_info
from functions.get_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_file import run_python_file, schema_run_python_file
from config import work_dir

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def calling_function(function, verbose= False):
    if not verbose:
        print(f'Calling function: {function.name}')

    print(f'Calling function: {function.name}({function.args})')
    
    function_kit = {"get_files_info": get_files_info,
                 "get_file_content": get_file_content,
                 "write_file": write_file,
                 "run_python_file": run_python_file,}
    

    arguments = function.args
    arguments["working_directory"] = work_dir

    if function.name not in function_kit:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function.name,
                    response={"error": f'Unknown function: {function.name}'},
                )
            ],
        )
    
    result = function_kit[function.name](**arguments)

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function.name,
                    response={"result": {result}},
                )
            ],
        ) 
