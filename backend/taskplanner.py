import openai
from typing import List
from pydantic import BaseModel
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Replace hardcoded API key with environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Task(BaseModel):
    task_id: int
    description: str
    agent: str
    function_call: str

class TaskPlan(BaseModel):
    tasks: List[Task]
    original_request: str

SYSTEM_PROMPT = """You are a task planning assistant. Your job is to break down user requests into smaller, logical tasks.
For each task, determine which agent should be used and the corresponding function call.
The available agents are:
- csv_agent: for CSV and DataFrame operations
- sentiment_agent: for sentiment analysis
- email_agent: for sending emails
- browser_agent: for web browsing tasks

Each task must include:
- task_id: a unique identifier
- description: a clear description of the task
- agent: the agent that will handle the task
- function_call: the function to call for that agent, the function name is the same as the agent name

Return the response in json format exactly as follows:
{
  "tasks": [
    {
      "task_id": 1,
      "description": "task description",
      "agent": "csv_agent",
      "function_call": "csv_agent.clean_data"
    }
  ],
  "original_request": "original user request"
}"""

def plan_tasks(user_request: str) -> TaskPlan:
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_request}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response from the LLM
        task_data = json.loads(response.choices[0].message.content)
        tasks = [Task(**task) for task in task_data["tasks"]]
        return TaskPlan(tasks=tasks, original_request=user_request)
        
    except Exception as e:
        print(f"Error in plan_tasks: {str(e)}")
        return TaskPlan(
            tasks=[Task(task_id=1, description=f"Error: {str(e)}", agent="error", function_call="none")],
            original_request=user_request
        )

# if __name__ == "__main__":
#     user_request = 'Analyse the sentiment of this text: "Donald trump is doing a poor job as the president of united states"'
#     task_plan = plan_tasks(user_request)
#     print(task_plan.model_dump_json(indent=2))
