import ollama
import logging
import time
import json

class AgentCreator:
    def __init__(self, model="llama3.2"):
        self.model = model         # Init with model.

    # Generate agent from problem statement.
    def generate_agent(self, problem_statement):
        prompt = f"""
        You are an AI that generates structured agents in JSON format.
        **Return ONLY JSON. No explanations or extra text.**
        
        **Task:**
        - Create an agent that can solve the given problem.
        - Provide a role and a detailed role description.
        - Generate a specific task prompt for execution.
        - Include metadata like creation timestamp and LLM used.

        **JSON Format (Strict Schema):**
        ```json
        {{
    "role": "<Agent Role>",
    "role_description": "<Detailed agent role>",
    "task_prompt": "<Task details>",
    "parent_agent_id": "<ID of the parent agent (if applicable)>",
    "creation_timestamp": "<Unix timestamp>",
    "llm_used": "Llama 3.1"
        }}
        ```
        
        **Problem Statement:** "{problem_statement}"
        
        **Now, generate ONLY JSON output.**
        """

        try:
            response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            raw_text = response['message']['content'].strip()
            logging.debug("Raw response from Ollama: %s", raw_text)

            agent = json.loads(raw_text)
            # Set timestamp and model.
            agent["creation_timestamp"] = int(time.time())
            agent["llm_used"] = self.model

            return agent

        except Exception as e:
            logging.error("Error generating agent from model: %s", str(e), exc_info=True)
            return None
