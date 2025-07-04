import os
from google.genai import types
from config import work_dir


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    dir_abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not dir_abs_file_path.startswith(abs_working_dir):
         return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(dir_abs_file_path):
        try:
            os.makedirs(os.path.dirname(dir_abs_file_path), exist_ok=True)
        
        except Exception as e:
            return f'Error: creating dir to write file: {e}'
        
        if os.path.exists(dir_abs_file_path) and os.path.is_dir(dir_abs_file_path):
            return f'Error: {dir_abs_file_path} is a directory'
        
    try:
        with open(dir_abs_file_path, "w+") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:

        return f'Error: Cannot write to file: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description= "Writes to the file in the specified file_path (relative to the working_directory). If the file does not exists, it creates it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the file to be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is going to be written to the file at file_path.",
            ),
        },
        required=["file_path", "content"],
    ),
)