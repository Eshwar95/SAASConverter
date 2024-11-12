import os
from azure.search.documents import SearchClient
from openai.embeddings_utils import get_embedding
import openai
from azure.core.credentials import AzureKeyCredential
import getpass
import time

deployment_name="gpt-35-turbo-16k"
openai.api_type = "azure"
openai.api_key = "test"
openai.api_base = "https://myfirstopenaiplayground.openai.azure.com/"
openai.api_version = "2024-06-01"

if "AZURE_OPENAI_API_KEY" not in os.environ:
   os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass(
       "test"
   )
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://myfirstopenaiplayground.openai.azure.com/"

# Step 1: Generate Embeddings for Query
def get_query_embedding(query):
    return get_embedding(query, engine="text-embedding-ada-002")

# Step 2: Query Azure Search with Embedding
def query_azure_search_with_embedding(embedding):
    search_client = SearchClient(endpoint="https://genaitransformers-search.search.windows.net",
    index_name="vector-1731434530702",
    credential=AzureKeyCredential("test"))
    # Perform search using vector parameter in the latest SDK
    results = search_client.search(
        search_text="",  # Empty search text for vector search
        top=5
    )
    return [doc['chunk'] for doc in results]

# Helper function to summarize the conversation history
def summarize_history(conversation_history):
    summary = " ".join([item['content'] for item in conversation_history])
    return summary[:150]  # Limit summary to the first 500 tokens or adjust as needed

# Step 3: RAG (Combine Results and Generate Contextual Answer) using Chat API
def generate_answer(query, context, conversation_history, summary):
    # Create messages with condensed summary if available
    messages = [{"role": "system", "content": "You are a helpful assistant providing detailed responses."}]

    # Include summary if it exists
    if summary:
        messages.append({"role": "user", "content": f"Summary of previous context: {summary}"})

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
    conversation_history.append({"role": "assistant", "content": answer})

    return answer, conversation_history

# Main Function
def rag_pipeline(query, conversation_history, summary=""):
    # Generate embedding for the query
    embedding = get_query_embedding(query)

    # Retrieve relevant context from Azure Search
    retrieved_docs = query_azure_search_with_embedding(embedding)
    context = " ".join(retrieved_docs)

    # Generate contextual answer
    answer, updated_conversation_history = generate_answer(query, context, conversation_history, summary)
    return answer, updated_conversation_history, summary

# Example usage with conversation history and summary
conversation_history = []
summary = ""

queries=[
    "$Text"]

for query in queries:
    answer, conversation_history, summary = rag_pipeline(query, conversation_history, summary)
    print(f"Query: {query}")
    print(f"Answer: {answer}\n")
    time.sleep(10)