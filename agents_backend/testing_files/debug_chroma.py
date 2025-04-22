import os
import chromadb
import logging

logging.basicConfig(level=logging.DEBUG)

def debug_chroma_setup():
    try:
        # Get the absolute path
        current_dir = os.getcwd()
        db_path = os.path.join(current_dir, "chroma_db")
        print(f"Current working directory: {current_dir}")
        print(f"ChromaDB path: {db_path}")
        
        # Check if directory exists
        if os.path.exists(db_path):
            print(f"ChromaDB directory exists at: {db_path}")
            print("Contents:", os.listdir(db_path))
        else:
            print(f"ChromaDB directory does not exist at: {db_path}")
        
        # Try to initialize ChromaDB
        print("Initializing ChromaDB...")
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_or_create_collection("agents")
        
        # Add a test document
        collection.add(
            documents=["This is a test document"],
            metadatas=[{"source": "debug_script"}],
            ids=["test1"]
        )
        
        # Verify the document was added
        results = collection.get()
        print("\nCollection contents:", results)
        
    except Exception as e:
        print(f"Error during debug: {str(e)}")
        logging.exception("Debug error details:")

if __name__ == "__main__":
    debug_chroma_setup()