import base64
import streamlit as st
from streamlit_option_menu import option_menu

import CodeConversion as codeConvert

st.logo('Barclays_Logo.png')

def run():
    ""
    "# Welcome to SASVerter!"
    "The ultimate tool for seamless code conversion, automated testing, and comprehensive documentation generation."

    "Features:"
    "***Code Conversion***: Upload your code files and instantly convert them from one programming language to another with precision and accuracy."
    "***Unit Test Generation***: Automatically generate unit tests to ensure your code works as intended, saving you time and reducing errors."
    "***Documentation Creation***: Generate detailed and professional documentation for your code, making it easier to maintain and collaborate with your team."
    "Whether you’re migrating legacy code, optimizing your development process, or improving code quality, SASverter simplifies your workflow, allowing you to focus on what truly matters—writing great software."
    "Start now and streamline your coding journey today!"

with st.sidebar:
    app=option_menu(menu_title='SASverter', options=['HomePage','Documentaion Generator', 'Code Converter'], icons=['house-fill', 'book', 'laptop'])
if(app == 'Code Converter'):
    codeConvert.app()
if(app == 'HomePage'):
    # st.balloons()
    run()

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('Background.png')