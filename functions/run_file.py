import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
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
  



    
