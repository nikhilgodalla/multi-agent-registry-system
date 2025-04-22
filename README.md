# Implementation of Dynamic Subagent Creation & Role Assignment and Agent Registry & Metadata Database Modules

**Description:**  
To scale the **Super AI Agents Infrastructure**, we need to implement two core modules:  
1. **Dynamic Subagent Creation & Role Assignment**  
2. **Agent Registry & Metadata Database**  

These modules will work together to enable the creation of subagents dynamically based on problem statements, assign roles and tasks, and maintain a registry of all agents to avoid duplication. The system will use **Chroma DB** for agent metadata storage and **Neo4j** for graph-based agent-agent relationship management. The goal is to create a scalable, modular, and efficient infrastructure for agent creation and management.

---

### Key Features and Requirements:

#### **1. Dynamic Subagent Creation & Role Assignment Module:**
   - **Input:** Problem statement or query from an external agent.
   - **Output:** List of newly created subagents (if needed) with their roles, descriptions, and task prompts.
   - **Functionality:**
     - Dynamically create subagents based on the problem statement.
     - Assign roles, role descriptions, and task prompts to each subagent.
     - Use JSON output from LLMs to ensure structured and aligned agent creation.
     - Consult the **Agent Registry & Metadata Database** to avoid duplicate agents.
     - Handle multiple turns of agent creation with context from existing agents.
     - Send the final list of new agents (with parent-child relationships) to the Agent Registry for registration.
   - **Fields for Agent Creation (JSON):**
     - `agent_id`: Unique identifier for the agent.
     - `role`: The role of the agent in the multi-agent infrastructure.
     - `role_description`: A detailed description of the agent's role.
     - `task_prompt`: Dynamic task prompt generated based on the agent's role.
     - `parent_agent_id`: ID of the parent agent (if applicable).
     - `dependencies`: List of agents this agent depends on (e.g., siblings, other parent's children).
     - `metadata`: Additional metadata (e.g., creation timestamp, LLM used).

#### **2. Agent Registry & Metadata Database Module:**
   - **Functionality:**
     - Maintain a database of all agents in the ecosystem.
     - Use **Chroma DB** to store agent metadata (e.g., roles, descriptions, task prompts).
     - Use **Neo4j** to store agent-agent relationships (e.g., parent-child, dependencies).
     - Check for existing agents that can handle the task before creating new ones.
     - Register new agents with their metadata and relationships.
     - Handle complex agent dependencies (e.g., parent-child, sibling, cross-parent dependencies).
   - **Fields for Agent Registry (Chroma DB):**
     - `agent_id`: Unique identifier for the agent.
     - `role`: The role of the agent.
     - `role_description`: Description of the agent's role.
     - `task_prompt`: Task prompt assigned to the agent.
     - `creation_timestamp`: Timestamp of agent creation.
     - `llm_used`: LLM used for agent creation.
   - **Fields for Agent Relationships (Neo4j):**
     - `parent_agent_id`: ID of the parent agent.
     - `child_agent_id`: ID of the child agent.
     - `relationship_type`: Type of relationship (e.g., parent-child, sibling, dependency).

---

### Workflow:

1. **Problem Statement Input:**
   - An external agent sends a problem statement or query to the **Dynamic Subagent Creation & Role Assignment** module.

2. **Consult Agent Registry:**
   - The module consults the **Agent Registry & Metadata Database** to check if existing agents can handle the task.

3. **Agent Creation:**
   - If no existing agents can handle the task, the module dynamically creates new subagents.
   - Assigns roles, descriptions, and task prompts to each subagent.
   - Uses JSON output from LLMs for structured agent creation.

4. **Multiple Turns for Agent Creation:**
   - The module may require multiple turns to create agents, considering the context of existing agents.

5. **Register New Agents:**
   - Once all new agents are created, the module sends the final list (with metadata and relationships) to the **Agent Registry & Metadata Database** for registration.

6. **Handle Dependencies:**
   - The **Agent Registry** ensures that agent dependencies (e.g., parent-child, sibling, cross-parent) are correctly stored in Neo4j.

7. **Return Final Agent List:**
   - The **Dynamic Subagent Creation & Role Assignment** module returns the final list of agents (new and existing) to the external agent.

---

### Modules Dependencies:

1. **Dynamic Subagent Creation & Role Assignment Module:**
   - Depends on the **Agent Registry & Metadata Database** to check for existing agents and register new ones.
   - Uses LLM APIs (via Ollama) for agent creation and task prompt generation.

2. **Agent Registry & Metadata Database Module:**
   - Stores agent metadata in **Chroma DB**.
   - Manages agent-agent relationships in **Neo4j**.
   - Provides APIs for querying and registering agents.

---

### Implementation Guidelines:

1. **Modular Design:**
   - Keep the two modules separate but tightly integrated.
   - Use dependency injection for LLM API integration and database connections.

2. **Error Handling:**
   - Implement robust error handling for LLM calls, JSON parsing, and database operations.
   - Retry LLM calls if JSON output is invalid.

3. **Scalability:**
   - Design the system to handle a large number of agents and complex relationships.
   - Use efficient querying mechanisms for Chroma DB and Neo4j.

4. **Testing:**
   - Write unit tests for both modules.
   - Test edge cases (e.g., duplicate agents, complex dependencies).

5. **Documentation:**
   - Document the API endpoints, data structures, and workflows for both modules.
   - Provide examples for agent creation and registration.

---

### Acceptance Criteria:
1. Fully functional **Dynamic Subagent Creation & Role Assignment** module.
2. Fully functional **Agent Registry & Metadata Database** module.
3. Integration between the two modules.
4. Efficient use of Chroma DB and Neo4j for metadata and relationship storage.
5. Robust error handling and retry mechanisms.
6. Comprehensive documentation and unit tests.
