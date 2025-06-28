import os
from config import max_chars
from google.genai import types
from config import work_dir

def get_file_content(working_directory, file_path):
    working_directory = work_dir
    abs_working_dir = os.path.abspath(working_directory)
    dir_abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not dir_abs_file_path.startswith(abs_working_dir):
         return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(dir_abs_file_path):
         return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(dir_abs_file_path) as f:
            content = f.read(max_chars)
            if os.path.getsize(dir_abs_file_path) > max_chars:
                content += f'[...File "{file_path}" truncated at {max_chars} characters]'

        return content

    except Exception as e:

        return f"Error: Could'nt get content of {file_path}: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description= "Reads and returns the content of a file in the specified file_path. If it is bigger than 10000 characters, it truncates it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the file to be read, relative to the working directory.",
            ),
        },
    ),
)