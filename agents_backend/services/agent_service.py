import logging
from db.neo4j_db import (
    create_parent_agent_node,    # Used to create a new parent node if one doesn't exist.
    ensure_agent_node_exists,
    create_agent_node,
    create_relationship,
    get_agent_node_by_elementId,
    check_agents_exist,
    create_super_parent_node
      # Helper to retrieve an Agent node by its element id.
)
from db.chroma_db import ChromaDBManager
from agents.agent_creation import AgentCreator
from typing import Optional
class AgentService:
    def __init__(self):
        self.chroma_db = ChromaDBManager()    
        self.agent_creator = AgentCreator()   

    def process_problem(self, parent_id: Optional[str], statement: str) -> dict:

        agents_exist = check_agents_exist()
        if agents_exist and not parent_id:
            raise ValueError("parent_id is required when agents exist in the system")
    
        if not agents_exist and not parent_id:
            parent_id = create_super_parent_node()
            logging.info(f"Created super parent node with ID: {parent_id}")
        # First check if parent exists as an Agent
        existing_parent = get_agent_node_by_elementId(parent_id)
        
        if not existing_parent:
            # If not an Agent, create/ensure parent as DummyAgent
            parent_agent = {
                "agent_id": parent_id,
                "problem_statement": statement
            }
            create_parent_agent_node(parent_agent)
            logging.debug(f"Created DummyAgent parent with id: {parent_id}")

        # Check ChromaDB for similar agent
        similar_agent = self.chroma_db.retrieve_agent_by_problem(statement)
        if similar_agent:
            logging.info(f"Similar agent found: {similar_agent}")
            # Ensure the similar agent exists in Neo4j
            ensure_agent_node_exists(similar_agent)
            # Create relationship
            create_relationship(parent_id, similar_agent["elementId"])
            return {
                "message": "Existing agent found and mapped",
                "problem_statement": statement,
                "agent": similar_agent
            }

        # Generate new agent only if no similar agent found
        new_agent = self.agent_creator.generate_agent(statement)
        if not new_agent:
            raise Exception("Agent creation failed")

        # Add problem statement and clean up
        new_agent["problem_statement"] = statement
        new_agent.pop("agent_id", None)

        # Create Neo4j node and get elementId
        elementId = create_agent_node(new_agent)
        new_agent["elementId"] = elementId

        # Store in ChromaDB
        self.chroma_db.store_agent(new_agent)

        # Create relationship
        create_relationship(parent_id, elementId)

        return {
            "message": "New agent created and mapped",
            "problem_statement": statement,
            "agent": {
                "elementId": elementId,
                "role": new_agent.get("role"),
                "role_description": new_agent.get("role_description"),
                "task_prompt": new_agent.get("task_prompt")
            }
        }


