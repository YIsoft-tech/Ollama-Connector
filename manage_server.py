from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
tasks = {}
next_task_id = 1
RESULTS_FILE = 'results.csv'  # CSV file to store task results

# Reset the results file at startup
with open(RESULTS_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['task_id', 'result'])  # Header row

@app.route('/task', methods=['GET'])
def get_task():
    """ Sends the next task (prompt) to the local LLM server. """
    if tasks:
        task_id, task_data = next(iter(tasks.items()))
        return jsonify({
            'task_id': task_id,
            'prompt': task_data['prompt'],
            'model': task_data['model']  # Include the model name
        })
    return jsonify({}), 200

@app.route('/task', methods=['POST'])
def post_result():
    """ Receives the result of the LLM task from the local LLM server. """
    data = request.json
    task_id = data.get('task_id')
    result = data.get('result')

    if task_id in tasks:
        tasks[task_id]['result'] = result

        # Store the result in the CSV file
        with open(RESULTS_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([task_id, result])

        # Remove the task from memory
        del tasks[task_id]
        return jsonify({'message': 'Result received and stored.'}), 200

    return jsonify({'error': 'Task not found.'}), 404

@app.route('/submit', methods=['POST'])
def submit_task():
    """ Receives a prompt and model from the internet user and queues it for the local LLM. """
    global next_task_id
    data = request.json
    prompt = data.get('prompt')
    model = data.get('model', 'llama3')  # Default to "llama3" if no model is specified

    if not prompt:
        return jsonify({'error': 'No prompt provided.'}), 400

    task_id = next_task_id
    tasks[task_id] = {'prompt': prompt, 'model': model}
    next_task_id += 1

    return jsonify({'task_id': task_id, 'status': 'Task submitted.'}), 200

@app.route('/result/<int:task_id>', methods=['GET'])
def get_result(task_id):
    """ Returns the result of the given task if completed. """
    # Check if the result is in the CSV file
    with open(RESULTS_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if int(row[0]) == task_id:  # Compare with task_id
                return jsonify({'task_id': task_id, 'result': row[1]})
    return jsonify({'error': 'Task not found.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5201)
