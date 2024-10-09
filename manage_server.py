from flask import Flask, request, jsonify
import json

app = Flask(__name__)

tasks = {}
next_task_id = 1

@app.route('/task', methods=['GET'])
def get_task():
    """ Sends the next task (prompt) to the local LLM server. """
    global next_task_id
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
        del tasks[task_id]  # Remove the task after processing it
        return jsonify({'message': 'Result received.'}), 200
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
    task = tasks.get(task_id)
    if task:
        if 'result' in task:
            return jsonify({'task_id': task_id, 'result': task['result']})
        return jsonify({'task_id': task_id, 'status': 'Processing...'}), 200
    return jsonify({'error': 'Task not found.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
