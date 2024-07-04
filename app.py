from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    reminder = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    file = db.Column(db.String(100), nullable=True)
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    tasks = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', tasks=tasks)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = request.form.get('task')
    category = request.form.get('category')
    reminder = request.form.get('reminder')
    notes = request.form.get('notes')
    file = request.files.get('file')

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = None

    if reminder:
        reminder = datetime.strptime(reminder, '%Y-%m-%dT%H:%M')

    new_task = Todo(task=task, category=category, reminder=reminder, notes=notes, file=filename, complete=False, user_id=session['user_id'])
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = Todo.query.get(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = Todo.query.get(task_id)
    if task.file:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], task.file))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

@app.route('/reorder', methods=['POST'])
def reorder():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    sorted_ids = request.form.getlist('sortedIDs[]')
    for order, task_id in enumerate(sorted_ids):
        task = Todo.query.get(task_id)
        task.order = order
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    reminder = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    file = db.Column(db.String(100), nullable=True)
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)

# In the app initialization section
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Assign order to existing tasks if they don't have one
        tasks = Todo.query.all()
        for index, task in enumerate(tasks):
            if task.order is None:
                task.order = index
        db.session.commit()
    app.run(debug=True)
