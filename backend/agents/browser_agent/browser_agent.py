from typing import Dict, Optional
from openai import OpenAI
from browser_use import Agent
from langchain_openai import ChatOpenAI
import os
import asyncio
from dotenv import load_dotenv
import sys

load_dotenv()

async def search_web(query: str, max_results: int = 5, sort_by: Optional[str] = None) -> None:
    """
    Execute browser task without returning results
    
    Args:
        query: Full request from user (e.g., {"request": "find gaming laptops under 1000"})
        max_results: Number of results to return (default: 5)
        sort_by: How to sort results (e.g., "price", "rating")
    """
    try:
        # Extract the actual query from the request
        search_query = query.get("request") if isinstance(query, dict) else query
        
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        agent = Agent(
            task=search_query,
            llm=llm
        )
        
        # Just execute the task, don't return anything
        await agent.run()
        
    except Exception as e:
        print(f"Error during browser task: {str(e)}")

if __name__ == "__main__":
    # Get query from command line argument if provided
    query = sys.argv[1] if len(sys.argv) > 1 else "add a gaming laptop to cart on amazon"
    try:
        asyncio.run(search_web(query))
    except Exception as e:
        print(f"Test failed with error: {str(e)}") 