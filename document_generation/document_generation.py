#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:20:01 2024

@author: ayshwarya
"""

import openai
import pandas as pd
from docx import Document
import os
import getpass

deployment_name="gpt-35-turbo-16k"
openai.api_type = "azure"
openai.api_key = "test"#os.getenv("AZURE_OPENAI_API_KEY")  # Alternatively, paste your key directly: "your_api_key"
openai.api_base = "test"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2024-06-01"  # Ensure the API version matches the one in your Azure Portal

if "AZURE_OPENAI_API_KEY" not in os.environ:
   os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass(
       "test"
   )
os.environ["AZURE_OPENAI_ENDPOINT"] = "test"

def read_excel(file_path):
    """Read data from an Excel file."""
    df = pd.read_excel(file_path)
    return df

def generate_summary(data):
    """Generate sentences using OpenAI's GPT model."""
    prompt = f"Generate a summary for the following data:\n\n{data}\n\nSummary:"

    response = openai.chat.completions.create(
        model="gpt-35-turbo-16k",  # You can change the model if needed
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def create_word_document(content, output_file):
    """Create a Word document with the generated content."""
    doc = Document()
    doc.add_heading('Generated Summary', level=1)
    doc.add_paragraph(content)
    doc.save(output_file)

def main(excel_file, output_word_file):
    """Main function to read Excel, generate summary, and create Word document."""
    # Step 1: Read data from Excel
    data = read_excel(excel_file)

    # Step 2: Convert DataFrame to string format
    data_string = data.to_string(index=False)

    # Step 3: Generate summary using OpenAI API
    summary = generate_summary(data_string)

    # Step 4: Create a Word document with the summary
    create_word_document(summary, output_word_file)

if __name__ == "__main__":
    excel_file_path = '/Users/ayshwarya/Downloads/tests-example.xls'
    output_word_file_path = 'generated_file.docx'

    main(excel_file_path, output_word_file_path)
