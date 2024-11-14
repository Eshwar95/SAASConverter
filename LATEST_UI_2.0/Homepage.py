import base64
import streamlit as st
from streamlit_option_menu import option_menu
import CodeConversion as codeConvert
import Documentation as doc_generator

# Set page title and logo

st.set_page_config(page_title="IP-Unlocker", page_icon=":guardsman:", layout="wide")

# Function to display the login title and login form
def login():
    st.title('IP-Unlocker Login')  # Display the title for the login page
    
    # Define valid credentials
    correct_username = "demo"
    correct_password = "asdf"

    # Get username and password from user input
    username = st.text_input("Username", value="", max_chars=20)
    password = st.text_input("Password", type="password", value="", max_chars=20)

    # Create a login button
    if st.button('Login'):
        if username == correct_username and password == correct_password:
            # If credentials are correct, set login state and redirect
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()  # Trigger a rerun to update the page content
        else:
            st.error("Invalid username or password")

# Function to display the home page content after login
def run():
    st.title('IP-Unlocker: Unlocking Intellectual Property from Legacy Tech!')  # Display the main title after login
    st.markdown("""
    # Welcome to IP-Unlocker!
    The ultimate tool for seamless code conversion, automated testing, and comprehensive documentation generation.

    **Features**:
    - **Code Conversion**: Upload your code files and instantly convert them from one programming language to another with precision and accuracy.
    - **Unit Test Generation**: Automatically generate unit tests to ensure your code works as intended, saving you time and reducing errors.
    - **Documentation Creation**: Generate detailed and professional documentation for your code, making it easier to maintain and collaborate with your team.
    
    Whether you’re migrating legacy code, optimizing your development process, or improving code quality, IP-Unlocker simplifies your workflow, allowing you to focus on what truly matters—writing great software.
    Start now and streamline your coding journey today!
    """)

# Sidebar navigation
with st.sidebar:
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        app = option_menu(menu_title='IP-Unlocker', options=['HomePage', 'Documentation Generator', 'Code Converter'], icons=['house-fill', 'book', 'laptop'])
    else:
        app = None  # Skip the sidebar if the user is not logged in

# Check login status
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    # Show login form if not logged in
    login()
else:
    # Once logged in, show the app's main interface (HomePage by default)
    if app == 'HomePage' or not app:
        run()  # Display HomePage content directly after successful login

    if app == 'Code Converter':
        codeConvert.app()

    if(app =='Documentation Generator'):
        doc_generator.app()

# Function to convert an image file to base64 for background
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set the background image for the app
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background
# set_background('Background.png')
