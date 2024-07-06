from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    complete = db.Column(db.Boolean, default=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.deadline.asc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_data = request.form['task']
    deadline_data = request.form.get('deadline')
    description_data = request.form.get('description', '')

    if deadline_data:
        deadline_data = datetime.strptime(deadline_data, '%Y-%m-%dT%H:%M')

    new_task = Task(task=task_data, deadline=deadline_data, description=description_data)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task added successfully'})

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get_or_404(task_id)
    task.complete = not task.complete
    db.session.commit()
    return jsonify({'message': 'Task status updated'})

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.task = request.form['task']
        task.deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%dT%H:%M') if request.form['deadline'] else None
        task.description = request.form['description']
        db.session.commit()
        return jsonify(message='Task updated successfully')
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
