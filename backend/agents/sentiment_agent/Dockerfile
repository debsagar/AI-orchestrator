FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the agent code
COPY sentiment_agent.py .

# Command to run the agent
CMD ["python", "sentiment_agent.py"] 