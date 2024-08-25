import os
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize the ChromaDB client
client = chromadb.Client()

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create a collection in ChromaDB
collection = client.create_collection(name="html_docs")

def parse_html(html_content):
    """
    Parse the HTML and return documents split by tag.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    documents = []
    for tag in soup.find_all(True):  # True means any tag
        documents.append({
            'tag_name': tag.name,
            'content': tag.get_text(strip=True),
            'raw_html': str(tag)
        })
    
    return documents

def insert_documents_to_chromadb(documents):
    """
    Insert documents into ChromaDB, using tag content as embeddings.
    """
    for i, doc in enumerate(documents):
        # Compute embeddings
        embedding = model.encode(doc['content'], show_progress_bar=False)
        # Add document to ChromaDB collection
        collection.add(
            metadatas=[{
                'tag_name': doc['tag_name'],
                'raw_html': doc['raw_html']
            }], 
            documents=[doc['content']],
            ids=[str(i)]  # Unique IDs for each document
        )

def query_chromadb(query):
    """
    Query ChromaDB with a given search string.
    """
    
    results = collection.query(
        query_texts=[query],
        n_results=2  # Return top 5 results
    )
    
    return results


if __name__ == "__main__":
    # Path to the HTML file
    html_file_path = 'page_outputs\\test2.html'
    
    if not os.path.exists(html_file_path):
        print(f"File {html_file_path} not found!")
        exit()

    # Load HTML content
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse HTML and split into documents by tag
    documents = parse_html(html_content)
    
    # Insert the documents into ChromaDB
    insert_documents_to_chromadb(documents)
    
    # Query the database
    query = input("Enter your query: ")
    results = query_chromadb(query)
    
    # Display results
    for result in results['documents'][0]:
        print(result)
