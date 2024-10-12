
# LLM Server and Manage Server

This project consists of two main components: the **LLM Server** and the **Manage Server**. The LLM Server interacts with a local Ollama model API to process tasks, while the Manage Server, built with Flask, manages task submissions and results from the LLM Server. Below is a detailed guide on how to install, run, and use these servers.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Setting Up Ollama](#setting-up-ollama)
- [Running the Servers](#running-the-servers)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [File Descriptions](#file-descriptions)
- [License](#license)

## Requirements

- Python 3.7 or higher
- Flask
- Requests
- Ollama model server running locally

## Installation

1. **Clone the repository** (or download the code files):
   ```bash
   git clone <your_repository_url>
   cd <your_repository_directory>
   ```

2. **Install the required packages**:
   ```bash
   pip install Flask requests
   ```

## Setting Up Ollama

To set up the Ollama model server locally, follow these steps:

1. **Download Ollama** from the official website: [Ollama Download](https://ollama.com/download).
2. **Install the required models** by running the following command in your terminal (adjust the model name as needed):
   ```bash
   ollama pull llama3:70b
   ```
3. **Start the Ollama server** to serve the model:
   ```bash
   ollama serve
   ```
   Ensure the server runs on `http://localhost:11434/api/generate`.

## Running the Servers

1. Start the **Manage Server** (this will manage task submissions and results):
   ```bash
   python manage_server.py
   ```
   This server will run on port `5000` by default.

2. Start the **LLM Server** (this will poll the Manage Server for tasks):
   ```bash
   python llm_server.py
   ```
   This server will run continuously, checking for new tasks.

## How It Works

- The **Manage Server** allows users to submit tasks (prompts) via a POST request to the `/submit` endpoint. Each task is assigned a unique task ID.
- The **LLM Server** periodically polls the Manage Server to check for new tasks. When a task is found, it sends the prompt to the Ollama model for processing.
- Once the LLM Server receives a response, it sends the result back to the Manage Server, where it is stored and can be retrieved later.

## API Endpoints

### Manage Server Endpoints

- `POST /submit`:
  - **Description**: Submits a new task (prompt) for processing.
  - **Request Body**:
    ```json
    {
        "prompt": "Your prompt here",
        "model": "optional_model_name"  // Defaults to "llama3"
    }
    ```
  - **Response**:
    ```json
    {
        "task_id": 1,
        "status": "Task submitted."
    }
    ```

- `GET /task`:
  - **Description**: Retrieves the next task to be processed.
  - **Response**:
    ```json
    {
        "task_id": 1,
        "prompt": "Your prompt here",
        "model": "optional_model_name"
    }
    ```

- `POST /task`:
  - **Description**: Receives the result of a processed task.
  - **Request Body**:
    ```json
    {
        "task_id": 1,
        "result": "Result from LLM"
    }
    ```
  - **Response**:
    ```json
    {
        "message": "Result received."
    }
    ```

- `GET /result/<task_id>`:
  - **Description**: Retrieves the result of a completed task.
  - **Response**:
    ```json
    {
        "task_id": 1,
        "result": "Result from LLM"
    }
    ```

### LLM Server Endpoints

- This server doesn't expose public endpoints but communicates with the Manage Server via its defined API.

## File Descriptions

### `llm_server.py`

- **Functionality**: This script interacts with the local Ollama model to process tasks.
- **Main Functions**:
  - `call_ollama(model, prompt)`: Calls the Ollama API with the specified model and prompt.
  - `check_for_task()`: Polls the Manage Server for new tasks.
  - `send_result_to_azure(task_id, result)`: Sends the processed result back to the Manage Server.

### `manage_server.py`

- **Functionality**: This Flask app manages task submissions and results for the LLM Server.
- **Main Endpoints**:
  - `GET /task`: Retrieves the next task for processing.
  - `POST /submit`: Receives and queues new tasks from users.
  - `POST /task`: Accepts results from the LLM Server.
  - `GET /result/<task_id>`: Returns the result of a completed task.

### `test.py`

- **Functionality**: This script interacts with the Manage Server to submit tasks and wait for results.
- **Main Functions**:
  - `submit_task(prompt, model)`: Submits a new task to the Manage Server.
  - `wait_for_result(task_id)`: Polls the Manage Server for the result of the submitted task.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.