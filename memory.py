import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

# 1. Load Secrets
load_dotenv()

# 2. Setup the "Translator" (Embeddings)
print("🧠 Loading Embedding Model...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# 3. Setup the Database Connection
index_name = "competitor-brain"

def save_to_memory(company_name: str, report_text: str):
    """Saves a mission report to the long-term memory."""
    try:
        # Create a "Document" (Text + Metadata)
        doc = Document(
            page_content=report_text,
            metadata={"source": "competitor_spy", "company": company_name}
        )
        
        # Connect to Pinecone
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        
        # Save it
        vectorstore.add_documents([doc])
        print(f"✅ Successfully saved {company_name} to Pinecone!")
        return True
    except Exception as e:
        print(f"❌ Memory Error: {e}")
        return False

def search_memory(query: str):
    """Searches the vector DB for relevant past reports."""
    try:
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        # Search for the 3 most similar past reports
        results = vectorstore.similarity_search(query, k=3)
        
        # Combine them into a single text block
        context = "\n\n".join([doc.page_content for doc in results])
        return context
    except Exception as e:
        return f"Error retrieving memory: {e}"