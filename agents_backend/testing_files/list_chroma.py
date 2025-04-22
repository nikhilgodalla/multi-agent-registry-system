# list_chroma.py
import logging
import chromadb
import os

logging.basicConfig(level=logging.DEBUG)

def list_all_agents():
    """
    Retrieves and prints all agents stored in the ChromaDB 'agents' collection.
    """
    try:
        # Get absolute path
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "chroma_db")
        client = chromadb.PersistentClient(path=db_path)

        
        # Initialize the PersistentClient
        client = chromadb.PersistentClient(path=db_path)
        print("ChromaDB client initialized successfully")
        
        # Get the collection
        collection = client.get_or_create_collection("agents")
        print("Retrieved 'agents' collection")
        
        # Get all items
        agents = collection.get()
        print("\nRaw collection data:", agents)
        
        # Process results
        ids = agents.get("ids", [])
        documents = agents.get("documents", [])
        metadatas = agents.get("metadatas", [])
        
        if not ids:
            print("\nNo agents found in the database.")
            return
        
        print("\nListing all agents in ChromaDB:")
        for idx, agent_id in enumerate(ids):
            print(f"\nAgent {idx + 1}:")
            print(f"  ID: {agent_id}")
            
            if idx < len(documents):
                print(f"  Document: {documents[idx]}")
            else:
                print("  Document: N/A")
            
            if idx < len(metadatas):
                print(f"  Metadata: {metadatas[idx]}")
            else:
                print("  Metadata: N/A")
            
    except Exception as e:
        logging.error("Error listing agents:", exc_info=True)
        print(f"An error occurred while retrieving agents: {str(e)}")

if __name__ == "__main__":
    list_all_agents()
