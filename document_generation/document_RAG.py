import os
from azure.search.documents import SearchClient
from openai.embeddings_utils import get_embedding
import openai
import getpass
from azure.core.credentials import AzureKeyCredential

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

# Step 1: Generate Embeddings for Query
def get_query_embedding(query):
    return get_embedding(query, engine="text-embedding-ada-002")

# Step 2: Query Azure Search with Embedding
def query_azure_search_with_embedding(embedding):
    search_client = SearchClient(
        endpoint="https://genaitransformers-search.search.windows.net",
        index_name="vector-test",
        credential=AzureKeyCredential("test"))

    results = search_client.search(
        search_text="",
        top=5
    )
    return [doc['chunk'] for doc in results]

# Step 3: RAG (Combine Results and Generate Answer) using Chat API
def generate_answer(query, context):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Answer the question based on the context below.\n\nContext: {context}\n\nQuestion: {query}"}
    ]
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo-16k",
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# Main Function
def rag_pipeline(query):
    # Generate embedding for the query
    embedding = get_query_embedding(query)

    # Retrieve relevant context from Azure Search
    retrieved_docs = query_azure_search_with_embedding(embedding)
    context = " ".join(retrieved_docs)

    # Generate answer based on context
    answer = generate_answer(query, context)
    return answer

# Example usage
query = "What are the installation steps in the document?"
answer = rag_pipeline(query)
print("Answer:", answer)
