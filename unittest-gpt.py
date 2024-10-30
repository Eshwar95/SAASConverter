import os
from openai import AzureOpenAI
import zipfile
from pathlib import Path

def extractFolder(filepath,extractedPath):
    with zipfile.ZipFile(filepath, 'r') as zObject:
        zObject.extractall(path=extractedPath)
    # Convert extractedPath to a Path object
    dir_path = Path(extractedPath+'\\testcode')

    return dir_path

def generate_respone(filecontent):
    try:
        client = AzureOpenAI(
            api_key="API_KEY",
            api_version="version",
            azure_endpoint='AZUREURL'
            )
        chat_completion = client.chat.completions.create(
            model="gpt", # model = "deployment_name".
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
    for file_path in dir_path.iterdir():
        if file_path.is_file():
            # generate_respone(file_path)
            f = open(file_path, "r")
            filename = os.path.basename(file_path)
            response = generate_respone(f.read())
            write_to_file(test_directory_path,response, filename)
            # print(f'Processing file: {file_path}')
    print('Test Generation Completed!')


file_path = r'C:\Users\User\Desktop\Learning\HackathonPrep\testcode.zip'
extractedPath = r'C:\Users\User\Desktop\Learning\HackathonPrep\testcode'
process_model(file_path, extractedPath)
