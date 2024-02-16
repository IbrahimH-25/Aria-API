from flask import Flask, jsonify, request

app = Flask(__name__)

# A simple in-memory datastore to store tasks.
tasks = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, Cheese, Pizza, Fruit, Tylenol", "done": False},
    {"id": 2, "title": "Learn Python", "description": "Need to find a good Python tutorial on the web", "done": False}
]

# A route to get all tasks.
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# A route to get a single task by ID.
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    print('g')
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is not None:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

# A route to create a new task.
@app.route('/api/tasks', methods=['POST'])
def create_task():
    print('c',request.json)
    if 'title' in request:
        print('title')
    if not request.json:
        print('nrequest')
    if not request.json or not 'title' in request.json:
        return jsonify({"error": "Bad request"}), 400
    task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify(task), 201

# A route to update a task.
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    print('u')
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['done'] = request.json.get('done', task['done'])
    return jsonify(task)

# A route to delete a task.
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    print('d')
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
