import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.agent_service import AgentService  # Updated import path
from typing import Optional  # Add this import

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create FastAPI app instance
app = FastAPI()

# Global instance of our service
agent_service = AgentService()

# Pydantic model for incoming requests
class ProblemStatementRequest(BaseModel):
    parent_id: Optional[str] = None  # Modified this line
    problem_statement: str

    class Config:
        schema_extra = {
            "example": {
                "parent_id": "parent123",
                "problem_statement": "Analyze market trends"
            }
        }

@app.post("/submit_problem/")
async def receive_problem(problem: ProblemStatementRequest):
    statement = problem.problem_statement.strip()
    parent_id = problem.parent_id.strip() if problem.parent_id else None  # Modified this lin

    if not statement:
        raise HTTPException(status_code=400, detail="Problem statement cannot be empty")
    #if not parent_id:
        #raise HTTPException(status_code=400, detail="Parent ID cannot be empty")

    try:
        result = agent_service.process_problem(parent_id, statement)
        return result
    except ValueError as ve:  # Add specific handling for ValueError
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Error processing problem: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
