from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To silence a warning
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    try:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        logging.error(f"Error loading tasks: {e}")
        return 'There was an issue loading the tasks'

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['content']
    if not task_content:
        logging.error("Task content is empty")
        return 'Task content cannot be empty'
    
    new_task = Todo(content=task_content)
    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        logging.error(f"Error adding task: {e}")
        return 'There was an issue adding your task'

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        logging.error(f"Error deleting task: {e}")
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        if not task.content:
            logging.error("Updated task content is empty")
            return 'Task content cannot be empty'
        
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            logging.error(f"Error updating task: {e}")
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
