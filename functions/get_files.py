import os

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    dir_abs_path = os.path.abspath(os.path.join(working_directory, directory))

    if not dir_abs_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(dir_abs_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        content = []
        for file in os.listdir(dir_abs_path):
            file_path = os.path.join(dir_abs_path, file)
            content.append(f'{file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}')
        
        return "\n".join(content)
    except Exception as e:
        return f"Error when getting files: {e}"