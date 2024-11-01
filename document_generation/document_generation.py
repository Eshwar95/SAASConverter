#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:20:01 2024

@author: ayshwarya
"""

import pandas as pd
from docx import Document

def excel_to_word(excel_file, word_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Create a new Word Document
    doc = Document()
    doc.add_heading('Excel Data', level=1)a

    # Add a table to the Word document
    table = doc.add_table(rows=1, cols=len(df.columns))
    table.style = 'Table Grid'

    # Add column headers
    hdr_cells = table.rows[0].cells
    for i, column in enumerate(df.columns):
        hdr_cells[i].text = str(column)

    # Add data rows
    for index, row in df.iterrows():
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)

    # Save the Word document
    doc.save(word_file)
    print(f"Data has been written to {word_file}")

# Example usage
if __name__ == "__main__":
    excel_file = '/Users/ayshwarya/Downloads/tests-example.xls'  # Replace with your Excel file path
    word_file = 'output.docx'   # Output Word file path
    excel_to_word(excel_file, word_file)
