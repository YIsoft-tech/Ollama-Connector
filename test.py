import requests
import time

# Management server URL
MANAGEMENT_SERVER_URL = 'http://192.168.1.129:5000/submit'
RESULT_SERVER_URL = 'http://192.168.1.129:5000/result'  # URL to get the result of the task

def submit_task(prompt, model='llama3'):
    """ Submits the task to the management server. """
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": prompt,
        "model": model
    }
    
    try:
        response = requests.post(MANAGEMENT_SERVER_URL, headers=headers, json=data)
        if response.status_code == 200:
            task_id = response.json().get('task_id')
            print("Task submitted successfully. Task ID:", task_id)
            return task_id
        else:
            print(f"Failed to submit task: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"Error submitting task: {e}")
        return None

def wait_for_result(task_id):
    """ Waits for the result of the task. """
    while True:
        try:
            response = requests.get(f"{RESULT_SERVER_URL}/{task_id}")
            if response.status_code == 200:
                data = response.json()
                print("Result received:", data['result'])
                break
            elif response.status_code == 404:
                print("Task not found. It may not have been processed yet. Waiting...")
            else:
                print(f"Failed to get result: {response.status_code}")
            time.sleep(1)  # Wait before checking again
        except Exception as e:
            print(f"Error fetching result: {e}")
            break

if __name__ == '__main__':
    # Ask user for prompt and model
    prompt = input("Enter the prompt: ")
    model = input("Enter the model (default is 'llama3'): ") or 'llama3'
    
    # Submit task to management server
    task_id = submit_task(prompt, model)
    
    if task_id:
        # Wait for the result of the task
        wait_for_result(task_id)
