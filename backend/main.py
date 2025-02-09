from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional
import backend.taskplanner as taskplanner
import backend.orchestrator as orchestrator
from fastapi.responses import JSONResponse

app = FastAPI()

class UserRequest(BaseModel):
    request: str
    data: Optional[str] = None

@app.post("/process_request")
async def process_request(user_request: UserRequest):
    # Get task plan
    task_plan = taskplanner.plan_tasks(user_request.request)
    
    # Execute tasks with data if provided
    results = await orchestrator.orchestrate(task_plan, user_request.data)
    
    return JSONResponse(content={
        "message": "Request processed",
        "task_plan": task_plan.model_dump(),
        "results": results
    })

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    return JSONResponse(content={"task_id": task_id, "status": "Processing"})

@app.get("/results/{task_id}")
async def get_results(task_id: str):
    return JSONResponse(content={"task_id": task_id, "results": "Result data placeholder"})
