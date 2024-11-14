
import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import openai
import getpass
from azure.search.documents import SearchClient
from openai.embeddings_utils import get_embedding
from azure.core.credentials import AzureKeyCredential
import time

deployment_name="gpt-35-turbo-16k"
openai.api_type = "azure"
openai.api_key = "test" 
openai.api_base = "https://test.openai.azure.com/"  
openai.api_version = "2024-06-01"  

if "AZURE_OPENAI_API_KEY" not in os.environ:
   os.environ["AZURE_OPENAI_API_KEY"] = "test"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://test.openai.azure.com/"

# Set up your Azure Storage account credentials
AZURE_STORAGE_CONNECTION_STRING = "test"  # Your connection string here
  
CONTAINER_NAME = "genaicontainer"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# Function to upload file to Azure Blob Storage
def upload_file_to_azure(file, filename):
    try:
        # Get the container client
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # Create a blob client to interact with the container
        blob_client = container_client.get_blob_client(filename)
        
        # Upload the file
        blob_client.upload_blob(file, overwrite=True)
        return True
    except Exception as e:
        return False

# Step 1: Generate Embeddings for Query
def get_query_embedding(user_query):
    return get_embedding(user_query, engine="text-embedding-ada-002")

# Step 2: Query Azure Search with Embedding
def query_azure_search_with_embedding(embedding):
    search_client = SearchClient(endpoint="httpstest",
    index_name="test-test",
    credential=AzureKeyCredential("test"))
    # Perform search using vector parameter in the latest SDK
    results = search_client.search(
        search_text=user_query,  # Empty search text for vector search
        top=5
    )
    return [doc['chunk'] for doc in results]

# Main Function
def rag_pipeline(query):
    # Generate embedding for the query
    embedding = get_query_embedding(query)
    
    # Retrieve relevant context from Azure Search
    retrieved_docs = query_azure_search_with_embedding(embedding)
    context = " ".join(retrieved_docs)

    
    return context

def get_openai_response(query,context):

    messages = [{"role": "system", "content": "You are a helpful assistant providing detailed responses."}]
    
    # Add the current question and context
    messages.append({"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"})

    # Generate response
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo-16k",
        messages=messages,
        max_tokens=150  # Adjust max tokens as needed
    )
    
    # Get the assistant's response and add it to conversation history
    answer = response.choices[0].message['content'].strip()

    return answer
def app():

    # Streamlit interface
    st.title("Upload File and Ask Queries to OpenAI")

    if "uploaded" not in st.session_state:
        st.session_state["uploaded"] = False
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "user_query" not in st.session_state:
        st.session_state["user_query"] = ""

    # File upload widget
    uploaded_file = st.file_uploader("Choose a file", type=["java", "py", "txt", "csv", "js", "cs", "dat","xlsx", "docx"])

    # Button to upload file to Azure
    if uploaded_file is not None:
        st.write(f"Filename: {uploaded_file.name}")
        if st.button("Upload to Azure"):
            if upload_file_to_azure(uploaded_file, uploaded_file.name):
                st.success(f"File '{uploaded_file.name}' uploaded successfully to Azure Blob Storage!")
                st.session_state["uploaded"] = True  # Set the upload flag to True

    # Show the chat interface only if the file was successfully uploaded
    if st.session_state["uploaded"]:
        st.subheader("Interactive Chat with OpenAI")

        # Display chat history
        for message in st.session_state["chat_history"]:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI:** {message['content']}")

        # Text area for user query (use st.text_area instead of st.text_input)
        user_query = st.text_area("Enter your message:", value=st.session_state["user_query"], height=100)

        # If user submits a new query
        if st.button("Send"):
            if user_query.strip():
                # Append user's message to chat history
                st.session_state["chat_history"].append({"role": "user", "content": user_query})
                st.session_state["user_query"] = ""  # Reset input for next message

                # Get response from OpenAI and append it to chat history
                with st.spinner('Getting response from OpenAI...'):
                    context = rag_pipeline(user_query)
                    ai_response = get_openai_response(user_query, context)
                    st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})
                
                # Clear the input area
                st.session_state["user_query"] = ""
                st.rerun()

    time.sleep(10) 