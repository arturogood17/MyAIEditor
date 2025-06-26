import os
from config import max_chars

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    dir_abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not dir_abs_file_path.startswith(abs_working_dir):
         return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(dir_abs_file_path):
         return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        truncated_file = []
        with open(dir_abs_file_path) as f:
            truncated_file.append(f.read(max_chars))
            length= f.seek(0, 2)  
            if length > 10000:
                truncated_file.append(f'...File "{file_path}" truncated at 10000 characters')

        return " ".join(truncated_file)

    except Exception as e:

        return f"Error: Could'nt get content of {file_path}: {e}"                   