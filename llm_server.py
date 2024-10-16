import time
import requests

# Your Azure Web App URL
AZURE_WEB_APP_URL = 'https://341c4afa-8bf5-4be0-98cc-58fcaa34ec3d-00-3h6liyqmowb1.worf.replit.dev/task'

# Ollama local server URL
OLLAMA_API_URL = 'http://localhost:11434/api/generate'

def call_ollama(model, prompt):
    """ Calls the Ollama API on the local machine with the given model and prompt. """
    payload = {
        "model": model,  
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get('response', '').strip()
    else:
        print(f"Error in Ollama API: {response.status_code}")
        return ""

def check_for_task():
    """ Polls the Azure server to check if there's a task (prompt) to process. """
    try:
        response = requests.get(AZURE_WEB_APP_URL)
        if response.status_code == 200:
            data = response.json()
            if 'prompt' in data:
                prompt = data['prompt']
                model = data.get('model', 'llama3')  # Default model if not provided
                print(f"Received task with prompt: {prompt} using model: {model}")
                result = call_ollama(model, prompt)
                send_result_to_azure(data['task_id'], result)
    except Exception as e:
        print(f"Error fetching task: {e}")

def send_result_to_azure(task_id, result):
    """ Sends the result of the LLM processing back to the Azure server. """
    try:
        response = requests.post(AZURE_WEB_APP_URL, json={'task_id': task_id, 'result': result})
        if response.status_code == 200:
            print(f"Result for task {task_id} sent successfully.")
        else:
            print(f"Failed to send result: {response.status_code}")
    except Exception as e:
        print(f"Error sending result: {e}")

if __name__ == '__main__':
    while True:
        check_for_task()
        time.sleep(0.5)  # Poll every 1/2 seconds
