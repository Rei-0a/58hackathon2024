from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.due_date).all()  # 日付順にソート
    return render_template('app.html', tasks=tasks)

@app.route('/tasks/<id>')
def show_task(id):
    # idのタスクだけ取る
    #tasks = Task.query.order_by(Task.due_date).all() 
    
    task = Task.query.get(id)  # 個別にとる
    
    # show page
    return render_template('task_popup.html', task=task)

@app.route('/nextpage/')
def nextpage():
    return render_template('nextpage.html')

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    due_date = datetime.fromisoformat(request.form['due_date'])
    new_task = Task(title=title, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
