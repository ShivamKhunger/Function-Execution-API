# Automation API Service

A Python-based API service that uses LLM + RAG (Retrieval-Augmented Generation) to map user prompts to automation functions, generate executable Python code, and execute tasks like opening applications or monitoring system resources.

## Features
- **Function Registry**: Predefined automation tasks (e.g., open Chrome, Notepad, check CPU usage).
- **RAG Integration**: Uses SentenceTransformer and ChromaDB for prompt-to-function mapping.
- **Dynamic Code Generation**: Creates executable Python scripts on the fly.
- **Context Awareness**: Maintains session history for better responses.
- **API**: FastAPI endpoint for task execution and custom function addition.

## Setup
1. **Prerequisites**:
   - Python 3.11+
   - Git

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/automation-api.git
   cd automation-api
   