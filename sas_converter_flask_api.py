import zipfile
import os
import openai
import time
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# OpenAI API configuration
deployment_name = "gpt-35-turbo-16k"
openai.api_type = "azure"
openai.api_key = "fdf"  # Replace with your API key or set it as an environment variable
openai.api_base = "https://myfirstopenaiplayground.openai.azure.com/"
openai.api_version = "2024-06-01"

# Function to extract the contents of a zip file
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted contents to {extract_to}")

# Function to read the content of a file
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                content = file.read()
                return content
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

# Function to write code to a .py file in the output folder
def write_converted_file(output_folder, file_name, code, output_ext=".py"):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file_name + output_ext)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(code)
    print(f"Written converted code to {output_path}")
    return output_path

# Function to get converted code from OpenAI based on input language
def get_converted_code_from_openai(content, input_language, output_language):
    prompt = f"Generate {output_language} code by converting the following {input_language} code:\n\n{content}"
    
    try:
        messages = [
            {"role": "system", "content": f"You are an AI that generates {output_language} code."},
            {"role": "user", "content": prompt}
        ]
    
        # response = openai.ChatCompletion.create(
        #     engine=deployment_name,
        #     messages=messages,
        #     max_tokens=3000,
        #     temperature=0.7
        # )
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
def process_files(zip_path, extract_to, input_language, output_language):
    extract_zip(zip_path, extract_to)
    
    target_extension = f".{input_language.lower()}"
    output_folder = "converted_output"
    output_paths = []  # To store the paths of all converted files
    
    for root, _, files in os.walk(extract_to):
        for file_name in files:
            # Skip hidden files and system files like .DS_Store
            if file_name.startswith("."):
                print(f"Skipping hidden or system file: {file_name}")
                continue
            
            file_path = os.path.join(root, file_name)
            
            # Check if file has the correct extension for conversion
            if file_name.endswith(target_extension):
                print(f"Processing file: {file_name}")
                
                content = read_file(file_path)
                if content is None:
                    print(f"Skipping file {file_name} due to read errors.")
                    continue
                
                converted_code = get_converted_code_from_openai(content, input_language, output_language)
                if converted_code:
                    file_base_name = os.path.splitext(file_name)[0]
                    output_path = write_converted_file(output_folder, file_base_name, converted_code)
                    output_paths.append(output_path)
                
                time.sleep(10)
            else:
                print(f"File {file_name} does not match input language '{input_language}' and is skipped.")
    
    # Return an error if no valid files were processed
    if not output_paths:
        raise ValueError(f"No files with the specified input language: '{input_language}' were found for conversion.")
    
    return output_paths

@app.route('/convert', methods=['POST'])
def convert_code():
    try:
        # Retrieve the zip file and language settings from the request
        zip_file = request.files.get('zip_file')
        input_language = request.form.get("input_language")
        output_language = request.form.get("output_language")
        
        # Check if required fields are present
        if not zip_file or not input_language or not output_language:
            return jsonify({"error": "Missing required fields (zip_file, input_language, output_language)"}), 400
        
        # Save the uploaded zip file to a temporary location
        zip_path = "temp.zip"
        zip_file.save(zip_path)
        
        # Process files and convert to the specified language
        extract_folder = "extracted_files"
        output_paths = process_files(zip_path, extract_folder, input_language, output_language)
        
        return jsonify({
            "message": "Conversion completed successfully!",
            "output_paths": output_paths
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error in /convert endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
