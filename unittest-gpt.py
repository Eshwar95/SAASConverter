import os
from openai import AzureOpenAI
import zipfile
from pathlib import Path

def extractFolder(filepath,extractedPath):
    with zipfile.ZipFile(filepath, 'r') as zObject:
        zObject.extractall(path=extractedPath)
    # Convert extractedPath to a Path object
    dir_path = Path(extractedPath+'\\test_code')
    return dir_path

def read_folder():
    for root, dirs, files in os.walk(dir):
        for name in files:
            print(name)
            return 0
    return 1

def generate_respone(filecontent):
    try:
        client = AzureOpenAI(
            api_key="key",
        api_version="version",
        azure_endpoint='endpoint'
            )
        chat_completion = client.chat.completions.create(
            model="model", # model = "deployment_name".
            messages=[
                { "role": "system", "content": "Generate unit tests for the python code provided. Provide only the code, do not provide any explanations" },
                {
                    "role": "user",
                    "content": filecontent,
                },
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return None

def write_to_file(test_directory_path, text_content,file_name):
    f = open(test_directory_path+'\\test_'+file_name, "a")
    f.write(text_content)

def process_model(file_path,extractedPath ):
    dir_path = extractFolder(file_path,extractedPath)
     # Iterate through the extracted files
    test_directory_path=''
    test_directory_path = extractedPath +r'\Unit_Tests'
    try:
        print('Creating Unit Test Directory')
        os.makedirs(test_directory_path, exist_ok=True)  # exist_ok=True prevents an error if the directory already exists
        print(f'Directory created: {test_directory_path}')
    except Exception as e:
        print(f'Error creating directory: {e}')

    dir = extractedPath +'\\test_code'
    for root, dirs, files in os.walk(dir):
        for fileName in files:
            with open(os.path.join(root, fileName)) as f:
                response = generate_respone(f.read())
                write_to_file(test_directory_path,response, fileName)
                
    print('Test Generation Completed!')


file_path = r'\HackathonPrep\test_code.zip'
extractedPath = r"\HackathonPrep\test_code"
process_model(file_path, extractedPath)