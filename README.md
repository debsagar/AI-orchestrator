# AI-orchestrator

System Architecture: AI Task Orchestration System

![AI_Orchestrator](https://github.com/user-attachments/assets/006b060a-d4b7-4a10-9261-4ce48f60aa8d)

Core Components:

1. Frontend (Streamlit)
   - Simple, interactive web interface
   - File upload widgets
   - Status display
   - Real-time updates using Streamlit session state
   - Markdown rendering for results

2. Backend (FastAPI + Python)
   - Main API Server
   - Async request handling
   - File storage management
   - Response formatting for Streamlit

Key Components:

A. Task Planning Layer
   - TaskPlanner Module
     - Uses OpenAI GPT for task classification
     - Determines appropriate agent for task
     - Returns structured task plan
   - Supported task types:
     - Text analysis (sentiment)
     - Data cleaning (CSV)
     - Web automation (browser)
     - Medical image analysis

B. Orchestration Layer
   - Orchestrator Module
     - Task routing and execution
     - Async task management
     - Error handling
     - Result aggregation

C. Agent Layer
   1. Sentiment Agent
      - NLTK/OpenAI for sentiment analysis
      - Text processing pipeline
      - Emotion classification

   2. CSV Agent
      - Pandas for data cleaning
      - Missing value handling
      - Duplicate removal
      - Data validation

   3. Browser Agent
      - Async web automation
      - Browser-use library integration
      - Headless browser control
      - Web scraping capabilities

   4. Medical Agent
      - PyTorch for inference
      - Transformers library
      - Pre-trained skin lesion model
      - Image processing (PIL)

Data Flow:
1. User Input → Streamlit Frontend
2. Streamlit → FastAPI Backend
3. Backend → Task Planner
4. Task Planner → Orchestrator
5. Orchestrator → Specific Agent
6. Agent → Orchestrator
7. Orchestrator → Streamlit
8. Streamlit → User Display

Technologies:
- Frontend: Streamlit
- Backend: FastAPI, Python 3.9+
- ML/AI: PyTorch, Transformers, NLTK
- Data Processing: Pandas, Pillow
- Automation: Browser-use
- API: OpenAI GPT
- Storage: Local file system
- Communication: REST API

Key Features:
- Simple, intuitive UI with Streamlit
- File upload support
- Progress indicators
- Multi-modal input handling
- Extensible agent architecture
- Task classification
- Result visualization

Security:
- API key management via .env
- Input validation
- Error logging
- Secure file handling


