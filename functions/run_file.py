import os
import subprocess
from google.genai import types
from config import work_dir

def run_python_file(working_directory, file_path, args=None):
    working_directory = work_dir
    abs_working_dir = os.path.abspath(working_directory)
    dir_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not dir_abs_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(dir_abs_path):
        return f'Error: File "{file_path}" not found.'

    if not dir_abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    commands = ["python3", file_path]

    if args:
        commands.extend(args)

    try:    

        result= subprocess.run(commands, timeout=30, capture_output=True, cwd=working_directory, text=True)

        result_string = []

        if result.returncode != 0:
            result_string.append(f"Process exited with code {result.returncode}")

        if result.stdout:
            result_string.append(f"STDOUT: {result.stdout}")

        if result.stdout:
            result_string.append(f"STDERR: {result.stderr}")

        return " ".join(result_string) if result_string else "No output produced."
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
  
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description= "Runs the python file at the specified filepath (relative to the working_directory) with the provided arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the file to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments to run along the file at file_path. They are optional.",
            )
        },
    ),
)


    
