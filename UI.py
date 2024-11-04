import os
import zipfile
import openai
import time
import tempfile
from io import BytesIO
import subprocess
import streamlit as st
from pathlib import Path

# Set up OpenAI API configuration
openai.api_key = ""  # Securely set this 

# Streamlit custom styles
st.set_page_config(page_title="SAS Code & Unit Test Converter", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f9; color: #333; }
    .main-title { font-size: 36px; font-weight: 600; color: #336699; margin-top: 10px; margin-bottom: 20px; }
    .sub-title { font-size: 20px; font-weight: 400; color: #555; }
    .download-btn { background-color: #4CAF50; color: white; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>SAS Code & Unit Test Converter</h1>", unsafe_allow_html=True)
st.write("Convert SAS scripts to Python, C#, or Java, and optionally generate unit tests for the chosen language.")

# Function to extract contents of the zip file
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Read file content with encoding handling
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            return file.read()

# Clean and retain only executable code
def clean_code(code, language):
    lines = code.splitlines()
    cleaned_lines = []
    found_import = False
    for line in lines:
        if not found_import and (line.strip() == "" or line.strip().startswith("#") or "```" in line or "Here is the" in line):
            continue
        if not found_import and (line.strip().startswith("import") or language != "Python"):
            found_import = True
        if found_import:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

# Convert SAS code to desired language via OpenAI API
def get_code_from_openai(content, language):
    prompt = f"Convert the following SAS code to {language}:\n\n{content}"
    try:
        messages = [
            {"role": "system", "content": f"You are an AI that generates {language} code."},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.warning(f"Error with OpenAI API: {e}")
        return None

# Generate unit tests for the selected language via OpenAI API
def generate_unit_test(filecontent, language):
    try:
        prompt = f"Generate unit tests for the following {language} code. Provide only the code without any explanations:\n\n{filecontent}"
        messages = [
            {"role": "system", "content": f"You are an AI that generates {language} unit tests."},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.warning(f"Error generating unit tests: {e}")
        return None

# Process files in zip and retrieve converted code
def process_files(zip_file, language, generate_tests):
    with tempfile.TemporaryDirectory() as temp_dir:
        extract_zip(zip_file, temp_dir)
        converted_files = {}
        sas_files = [f for f in os.listdir(temp_dir) if f.endswith('.sas')]
        total_steps = len(sas_files) * (2 if generate_tests else 1)
        progress = st.progress(0)
        
        for i, file_name in enumerate(sas_files):
            file_path = os.path.join(temp_dir, file_name)
            content = read_file(file_path)
            
            # Code conversion step
            if content:
                code = get_code_from_openai(content, language)
                if code:
                    cleaned_code = clean_code(code, language)
                    converted_files[file_name] = cleaned_code
                    time.sleep(10)  # Delay for rate limits

            # Unit test generation step
            if generate_tests:
                unit_test_code = generate_unit_test(cleaned_code, language)
                if unit_test_code:
                    converted_files[file_name + "_test"] = unit_test_code
                progress.progress((i + 1) * 2 / total_steps)  # Update for unit test step
                
            # Update progress after each conversion and unit test (if applicable)
            progress.progress((i + 1) / total_steps)
        
        progress.empty()
        return converted_files

# Function to write and save unit tests
def save_unit_tests(converted_files, test_directory, file_extension):
    os.makedirs(test_directory, exist_ok=True)
    for filename, code in converted_files.items():
        with open(os.path.join(test_directory, filename), "w") as test_file:
            test_file.write(code)
    return True

# User upload zip file
uploaded_file = st.file_uploader("Upload a zip file with .sas files", type="zip", help="Upload a zip file containing your SAS files for conversion.")
language = st.selectbox("Choose the target language for conversion:", ["Python", "C#", "Java"])
generate_tests = st.checkbox("Generate unit tests for the chosen language")

# Determine the appropriate file extension based on the language
file_extension_map = {"Python": "py", "C#": "cs", "Java": "java"}
file_extension = file_extension_map[language]

# Conversion and unit test generation
if uploaded_file and language:
    if st.button("Start Conversion"):
        st.info("Processing files...")
        with tempfile.NamedTemporaryFile(delete=False) as tmp_zip:
            tmp_zip.write(uploaded_file.read())
            zip_file_path = tmp_zip.name
        converted_files = process_files(zip_file_path, language, generate_tests)
        
        if converted_files:
            output_zip = BytesIO()
            with zipfile.ZipFile(output_zip, 'w') as zf:
                for file_name, code in converted_files.items():
                    # Save only converted code files on screen, not unit tests
                    if "_test" not in file_name:
                        new_file_name = os.path.splitext(file_name)[0] + f"_converted.{file_extension}"
                        zf.writestr(new_file_name, code)
                        with st.expander(f"Converted Code: {file_name} ({language})"):
                            st.code(code, language=language.lower())
                    
                    # Save unit tests to zip only if generated
                    elif generate_tests:
                        new_test_name = os.path.splitext(file_name)[0] + f"_test.{file_extension}"
                        zf.writestr(new_test_name, code)

                output_zip.seek(0)

            st.download_button(
                label="📥 Download Converted Files and Unit Tests",
                data=output_zip,
                file_name="converted_and_tests.zip",
                mime="application/zip",
                key="download-btn"
            )
            st.success("Conversion complete! Download your files, including unit tests if selected.")
