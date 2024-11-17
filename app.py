from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Routes
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'completed': t.completed} for t in todos])

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = Todo(title=data['title'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'id': new_todo.id, 'title': new_todo.title, 'completed': new_todo.completed})

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    todo.completed = data.get('completed', todo.completed)
    db.session.commit()
    return jsonify({'message': 'Todo updated'})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
