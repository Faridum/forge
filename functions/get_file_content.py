import os

MAX_CHARS = 10000


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        valid_target_file = (os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs)

        if not valid_target_file:
            return (f'Error: Cannot read "{file_path}" '"as it is outside the permitted working directory")

        if not os.path.isfile(target_file):
            return (f'Error: File not found or is not a regular file: "{file_path}"')

        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)

            # Check whether there is still more content
            if f.read(1):
                content += (
                    f'\n[...File "{file_path}" '
                    f'truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: {e}"

def write_file(working_directory: str, file_path: str, content: str) -> str:    
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = (os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs)

        if not valid_target_file:
            return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        if os.path.isdir(target_file):
            return (f'Error: Cannot write to "{file_path}" as it is a directory')
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"