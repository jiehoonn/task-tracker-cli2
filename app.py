from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

todos = {}
next_id = 1

@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def get_task(todo_id):
    if todo_id not in todos:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todos[todo_id]), 200

@app.route("/api/todos", methods=["GET"])
def get_task_list():
    status = request.args.get("status", None)  # If no arg is provided, it defaults it None

    if status:
        filtered = {key: todo for key, todo in todos.items() if todo["status"] == status}
        return jsonify(filtered), 200

    return jsonify(todos), 200  # 200 OK successful fetch

@app.route("/api/todos", methods=["POST"])
def add_task():
    global next_id
    data = request.get_json()  # This reads the request body, parses the JSON body into a Python dictionary

    if not data:
        return jsonify({"error": "No data provided."}), 400
    if "description" not in data:
        return jsonify({"error": "Description is required."}), 400

    now = datetime.now(timezone.utc).isoformat()

    todo = {
        "id": next_id,
        "description": data["description"],
        "status": data.get("status", "not started"),  # Defaults to not started if not exists
        "createdAt": now,
        "updatedAt": now
    }

    todos[next_id] = todo
    next_id += 1

    return jsonify(todo), 201  # Successfully created

# When updating a task, the task_id is required. So we need the form /<int:todo_id>.
# Flask automatically checks that todo_id is of type int
@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_task(todo_id):
    if todo_id not in todos:
        return jsonify({"error": "ID not in task list"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    now = datetime.now(timezone.utc).isoformat()

    if "description" in data:
        todos[todo_id]["description"] = data["description"]
    if "status" in data:
        todos[todo_id]["status"] = data["status"]
    
    todos[todo_id]["updatedAt"] = now
    
    return jsonify(todos[todo_id]), 200  # 200 OK if returning response, 204 OK if not returning response

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_task(todo_id):
    if todo_id not in todos:
        return jsonify({"error": "ID does not exist in task list"}), 404

    del todos[todo_id]
    return jsonify({"message": f"Todo {todo_id} deleted successfully"}), 200  # 200 OK if returning response, 204 OK if not returning response

# Allows us to run this python file as a script through "python3 app.py"
if __name__ == "__main__":
    app.run(debug=True)