import logging
import json
import chromadb
import os 
class ChromaDBManager:
    def __init__(self):
        # Use the path relative to the db directory
        db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
        logging.info(f"Initializing ChromaDB with path: {db_path}")
        
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.agents_collection = self.chroma_client.get_or_create_collection(name="agents")

    def sanitize_metadata(self, value):
        # Convert metadata to a supported type.
        if isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, (dict, list)):
            return json.dumps(value)
        return str(value)

     # Store agent data in ChromaDB.
    def store_agent(self, agent_data):
        elementId = agent_data["elementId"]
        try:
            metadata = {
                "elementId": self.sanitize_metadata(agent_data.get("elementId", "")),
                "problem_statement": self.sanitize_metadata(agent_data.get("problem_statement", "")),
                "role": self.sanitize_metadata(agent_data.get("role", "Undefined Role")),
                "role_description": self.sanitize_metadata(agent_data.get("role_description", "")),
                "task_prompt": self.sanitize_metadata(agent_data.get("task_prompt", "")),
                "creation_timestamp": self.sanitize_metadata(agent_data.get("creation_timestamp", 0)),
                "llm_used": self.sanitize_metadata(agent_data.get("llm_used", "Unknown"))
            }

            description_text = (
                agent_data.get("role_description", "") + " " +
                self.sanitize_metadata(agent_data.get("task_prompt", ""))
            )

            self.agents_collection.add(
                ids=[elementId],
                documents=[description_text],
                metadatas=[metadata]
            )

            logging.debug("Stored Agent in ChromaDB with elementId: %s", elementId)
        except Exception as e:
            logging.error("Error Storing Agent in ChromaDB: %s", str(e), exc_info=True)
            raise

    def retrieve_agent_by_problem(self, problem_statement):
        # Retrieve agent from ChromaDB by problem statement.
        try:
            results = self.agents_collection.query(query_texts=[problem_statement], n_results=1)
            logging.debug("ChromaDB Query Results: %s", results)

            if results and "documents" in results and results["documents"]:
                similarity_scores = results.get("distances", [[1]])[0]
                best_score = similarity_scores[0] if similarity_scores else 1
                logging.debug("Similarity score for query '%s': %s", problem_statement, best_score)

                # Changed threshold to be less strict (from 0.7 to 0.85)
                SIMILARITY_THRESHOLD = 0.85
                if best_score > SIMILARITY_THRESHOLD:
                    logging.info(
                        "No sufficiently similar agent found (score %s > threshold %s).",
                        best_score, SIMILARITY_THRESHOLD
                    )
                    return None

                # Return more metadata about the found agent
                metadata = results.get("metadatas", [[]])[0][0]
                return {
                    "elementId": results.get("ids", [[]])[0][0],
                    "role": metadata.get("role"),
                    "role_description": metadata.get("role_description"),
                    "task_prompt": metadata.get("task_prompt")
                }

        except Exception as e:
            logging.error("Error retrieving agent by problem: %s", str(e), exc_info=True)
            return None

        return None
