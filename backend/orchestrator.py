import importlib
import asyncio
from typing import Dict, Any, Optional
import subprocess
import sys

async def execute_task(task: Any, user_request: str, data: str = None) -> Optional[Dict]:
    if task.agent == "sentiment_agent":
        try:
            from backend.agents.sentiment_agent import analyze_sentiment
            result = analyze_sentiment(user_request)
            return result
        except Exception as e:
            print(f"Error executing sentiment agent: {str(e)}")
            return {"error": str(e)}
            
    elif task.agent == "csv_agent":
        try:
            from backend.agents.csv_agent import clean_data
            result = clean_data(user_request, data)
            return result
        except Exception as e:
            print(f"Error executing CSV agent: {str(e)}")
            return {"error": str(e)}
            
    elif task.agent == "browser_agent":
        try:
            # Run browser_agent.py as a separate process
            subprocess.Popen([sys.executable, "backend/agents/browser_agent.py", user_request])
            return None
        except Exception as e:
            print(f"Error executing browser agent: {str(e)}")
            return {"error": str(e)}
    
    return {"error": f"Agent {task.agent} not implemented"}

async def orchestrate(task_plan: Any, data: str = None) -> Dict:
    if not task_plan.tasks:
        return {"error": "No tasks to execute"}
    
    task = task_plan.tasks[0]
    result = await execute_task(task, task_plan.original_request, data)
    
    # Special handling for browser tasks
    if task.agent == "browser_agent":
        return {
            "task_id": task.task_id,
            "message": "Browser task executed",
            "agent": "browser_agent"
        }
    
    return {"task_id": task.task_id, "result": result}

# Example usage:
# from task_planner import plan_tasks
# task_plan = await plan_tasks("Clean this dataset")
# result = orchestrate(task_plan.dict())
# print(result)
