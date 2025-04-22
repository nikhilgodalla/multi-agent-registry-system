from neo4j import GraphDatabase
import json
import logging
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# Initialize the Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

#It creates or updates a parent agent node in Neo4j using the external parent ID, and any new node is labeled "DummyAgent."
def create_parent_agent_node(agent_data):
    with driver.session() as session:
        session.execute_write(
            lambda tx: tx.run(
                """
                MERGE (d:DummyAgent {agent_id: $agent_id})
                SET d.problem_statement = $problem_statement
                """,
                agent_id=agent_data["agent_id"],
                problem_statement=agent_data["problem_statement"]
            )
        )

#  MERGE the agent node in Neo4j (for similar agents) using the composite identifier (elementId)
def ensure_agent_node_exists(agent_data):
    with driver.session() as session:
        session.execute_write(
            lambda tx: tx.run(
                """
                MERGE (a:Agent {elementId: $elementId})
                SET a.problem_statement = $problem_statement,
                    a.role = $role,
                    a.role_description = $role_description,
                    a.task_prompt = $task_prompt,
                    a.creation_timestamp = $creation_timestamp,
                    a.llm_used = $llm_used
                """,
                elementId=agent_data["elementId"],
                problem_statement=agent_data.get("problem_statement", ""),
                role=agent_data.get("role", "Undefined Role"),
                role_description=agent_data.get("role_description", ""),
                task_prompt=agent_data.get("task_prompt", ""),
                creation_timestamp=agent_data.get("creation_timestamp", 0),
                llm_used=agent_data.get("llm_used", "Unknown")
            )
        )

# Creates a new Agent node in Neo4j with the provided properties and returns its unique elementId.
def create_agent_node(agent_data):
    def _create_agent_node(tx, agent_data):
        query = """
            CREATE (a:Agent {
                elementId: randomUUID(),  // Add explicit elementId
                problem_statement: $problem_statement,
                role: $role,
                role_description: $role_description,
                task_prompt: $task_prompt,
                creation_timestamp: $creation_timestamp,
                llm_used: $llm_used
            })
            RETURN a.elementId AS elementId
        """
        result = tx.run(
            query,
            problem_statement=agent_data.get("problem_statement", ""),
            role=agent_data.get("role", "Undefined Role"),
            role_description=agent_data.get("role_description", ""),
            task_prompt=agent_data.get("task_prompt", ""),
            creation_timestamp=agent_data.get("creation_timestamp", 0),
            llm_used=agent_data.get("llm_used", "Unknown")
        )
        record = result.single()
        return record["elementId"]

    with driver.session() as session:
        element_id = session.execute_write(_create_agent_node, agent_data)
        return element_id



def create_relationship(parent_agent_id, child_agent_id):
    with driver.session() as session:
        session.execute_write(
            lambda tx: tx.run(
                """
                MATCH (p), (c:Agent {elementId: $child})
                WHERE (p:DummyAgent AND p.agent_id = $parent) 
                   OR (p:SuperParent AND p.id = $parent)
                MERGE (p)-[:DEPENDS_ON]->(c)
                """,
                parent=parent_agent_id,
                child=child_agent_id
            )
        )


# Retrieves an Agent node from Neo4j by its elementId.
def get_agent_node_by_elementId(element_id):
    def _get_agent_node(tx, element_id):
        query = """
            MATCH (a:Agent)
            WHERE elementId(a) = $id
            RETURN a
            LIMIT 1
        """
        result = tx.run(query, id=element_id)
        return result.single()
    
    with driver.session() as session:
        record = session.execute_read(_get_agent_node, element_id)
        if record:
            return record["a"]
        return None     #Returns the node record if found, or None otherwise.

def check_agents_exist():
    """
    Check if any Agent nodes exist in Neo4j.
    Returns True if agents exist, False otherwise.
    """
    with driver.session() as session:
        result = session.execute_read(
            lambda tx: tx.run(
                """
                MATCH (a:Agent)
                RETURN count(a) as count
                """
            ).single()
        )
        return result["count"] > 0

def create_super_parent_node():
    """
    Creates a super parent node in Neo4j.
    Returns the ID of the created node.
    """
    with driver.session() as session:
        result = session.execute_write(
            lambda tx: tx.run(
                """
                CREATE (s:SuperParent {
                    id: 'super_parent_' + randomUUID(),
                    created_at: datetime()
                })
                RETURN s.id as id
                """
            ).single()
        )
        return result["id"]
