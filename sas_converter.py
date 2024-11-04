import zipfile
import os
import openai
import time

# Set your OpenAI API key here
deployment_name="gpt-35-turbo-16k"
openai.api_type = "azure"
openai.api_key = "9c1a8daa826c4abab74f38cff791f231" #os.getenv("AZURE_OPENAI_API_KEY")  # Alternatively, paste your key directly: "your_api_key"
openai.api_base = "https://myfirstopenaiplayground.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2024-06-01"  # Ensure the API version matches the one in your Azure Portal

# Function to extract the contents of a zip file
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted contents to {extract_to}")

# Function to read the content of a file
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the file content
            content = file.read()
            # Return the content formatted as a string
            return f"""{content}"""
    except UnicodeDecodeError:
        # If there's a UnicodeDecodeError, try a different encoding
        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                content = file.read()
                return f"""{content}"""
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


# Function to write Python code to a .py file
def write_python_file(file_name, code):
    py_file_name = file_name + '.py'
    with open(py_file_name, 'w', encoding='utf-8') as file:
        file.write(code)
    print(f"Written Python code to {py_file_name}")

# Function to send file content to OpenAI and get the Python code
def get_python_code_from_openai(content):
    prompt = f"Generate python code by converting the following code:\n\n{content}"
    
    try:
        # # Send the content to OpenAI's GPT-35-turbo-16k API and get the response
        # response = openai.ChatCompletion.create(
        #     model="gpt-35-turbo-16k",  # Correctly specify the model parameter
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant that converts code to Python."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     max_tokens=3000,  # Adjust as necessary depending on expected output length
        #     temperature=0
        # )
        
        # # Get the generated Python code from the API response
        # python_code = response['choices'][0]['message']['content']
        # return python_code

        messages = [{"role": "system", "content": "You are an AI that generates Python code."},
        {"role": "user", "content": prompt}
        ]
    
        response = openai.ChatCompletion.create(
            engine=deployment_name,  # Replace with your deployment's engine name (e.g., gpt-3.5-turbo, gpt-4)
        messages=messages,
        max_tokens=200,  # Number of tokens for the response
        temperature=0.7  # Controls randomness; 0 is deterministic, 1 is highly random
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return None


# Main function to process each file in the extracted folder
def process_files(zip_path, extract_to):
    # Extract zip contents
    extract_zip(zip_path, extract_to)
    
    # Traverse the extracted folder
    for root, _, files in os.walk(extract_to):
        for file_name in files:
            # Skip hidden macOS system files (e.g., ._filename)
            if file_name.startswith("._"):
                print(f"Skipping hidden system file: {file_name}")
                continue
            
            file_path = os.path.join(root, file_name)
            
            # Check if file is a code file (e.g., .py, .java, .js, etc.)
            if file_name.endswith(('.py', '.java', '.js')):
                print(f"Processing file: {file_name}")
                
                # Read file contents
                content = read_file(file_path)
                
                # Skip files that couldn't be read
                if content is None:
                    print(f"Skipping file {file_name} due to read errors.")
                    continue
                
                # Send the content to OpenAI and get the Python code
                python_code = get_python_code_from_openai(content)
                print(python_code)
                if python_code:
                    # Remove the original file extension from the name and save as .py
                    file_base_name = os.path.splitext(file_name)[0]
                    write_python_file(file_base_name, python_code)
                
                # Add a delay to avoid hitting API rate limits
                time.sleep(10)


# Example usage
if __name__ == "__main__":
    zip_file_path = "/Users/eshwarvasudevan/Downloads/users_crud_app.zip"  # Provide the zip file path
    extract_folder = "converted_files"  # Folder to extract the contents into
    process_files(zip_file_path, extract_folder)
