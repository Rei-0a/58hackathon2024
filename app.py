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
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String(500), nullable=False)
    place = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Interview {self.title}>'

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String(500), nullable=False)
    place = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Meeting {self.title}>'

class Intern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String(500), nullable=False)
    place = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Intern {self.title}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()  # タスクをすべて取得
    interviews = Interview.query.all()
    meetings = Meeting.query.all()
    interns = Intern.query.all()  # インターンをすべて取得
    combined = []

    # タスクの情報を追加
    for task in tasks:
        combined.append((task.title, task.end_date, 'task',task.id))  # タスクの情報をタプルとして追加

    for interview in interviews:
        combined.append((interview.title, interview.end_date, 'interview',interview.id))

    for meeting in meetings:
        combined.append((meeting.title, meeting.end_date, 'meeting',meeting.id))
    
    for intern in interns:
        combined.append((intern.title, intern.end_date, 'intern',intern.id))  # インターンの情報をタプルとして追加

    # 日付でソート（タスクの締切日とインターンの開始日を比較）
    combined.sort(key=lambda x: (x[1] is None, x[1]))  # Noneを最後にし、日付でソート

    return render_template('app.html', combined=combined)

@app.route('/tasks/<id>')
def show_task(id):
    #type = request.args.get('type')

    # idのタスクだけ取る  
    task = Task.query.get(id)  # 個別にとる
    # show page
    return render_template('task_popup.html', task=task)

@app.route('/intern/<id>')
def show_intern(id):
    task = Intern.query.get(id)
    return render_template('intern_popup.html', task=task)

@app.route('/interview/<id>')
def show_interview(id):
    task = Interview.query.get(id)
    return render_template('interview_popup.html', task=task)

@app.route('/meeting/<id>')
def show_meeting(id):
    task = Meeting.query.get(id)
    return render_template('meeting_popup.html', task=task)


@app.route('/tasks/<id>/edit') #taskの編集
def task_edit(id):
    task = Task.query.get(id)
    return render_template('task_edit.html', task=task)

@app.route('/tasks/<id>/update', methods=['POST'])
def update_task(id):
    task = Task.query.get(id)
    title = request.form['title']
    task.title = title
    start_date = datetime.fromisoformat(request.form['start_date'])
    task.start_date = start_date
    end_date = datetime.fromisoformat(request.form['end_date'])
    task.end_date = end_date
    body = request.form['body']
    task.body = body
    db.session.commit()
    return redirect('/tasks/'+id)

@app.route('/interview/<id>/edit') #interviewの編集
def interview_edit(id):
    task = Interview.query.get(id)
    return render_template('interview_edit.html', task=task)

@app.route('/interview/<id>/update', methods=['POST'])
def update_interview(id):
    task = Interview.query.get(id)
    title = request.form['title']
    task.title = title
    start_date = datetime.fromisoformat(request.form['start_date'])
    task.start_date = start_date
    end_date = datetime.fromisoformat(request.form['end_date'])
    task.end_date = end_date
    body = request.form['body']
    task.body = body
    place = request.form['place']
    task.place = place
    db.session.commit()
    return redirect('/interview/'+id)

@app.route('/meeting/<id>/edit') #meetingの編集
def meeting_edit(id):
    task = Meeting.query.get(id)
    return render_template('meeting_edit.html', task=task)


@app.route('/meeting/<id>/update', methods=['POST'])
def update_meeting(id):
    task = Meeting.query.get(id)
    title = request.form['title']
    task.title = title
    start_date = datetime.fromisoformat(request.form['start_date'])
    task.start_date = start_date
    end_date = datetime.fromisoformat(request.form['end_date'])
    task.end_date = end_date
    body = request.form['body']
    task.body = body
    place = request.form['place']
    task.place = place
    db.session.commit()
    return redirect('/meeting/'+id)

@app.route('/intern/<id>/edit')  #internの編集
def intern_edit(id):
    task = Intern.query.get(id)
    return render_template('intern_edit.html', task=task)

@app.route('/intern/<id>/update', methods=['POST']) #internの編集後の情報更新
def update_intern(id):
    task = Intern.query.get(id)
    title = request.form['title']
    task.title = title
    start_date = datetime.fromisoformat(request.form['start_date'])
    task.start_date = start_date
    end_date = datetime.fromisoformat(request.form['end_date'])
    task.end_date = end_date
    body = request.form['body']
    task.body = body
    place = request.form['place']
    task.place = place
    db.session.commit()
    return redirect('/intern/'+id)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    start_date = datetime.fromisoformat(request.form['start_date'])
    end_date = datetime.fromisoformat(request.form['end_date'])
    body = request.form['body']
    new_task = Task(title=title, start_date=start_date, end_date=end_date, body=body)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/add_interview', methods=['POST'])
def add_interview():
    title = request.form['title']
    start_date = datetime.fromisoformat(request.form['start_date'])
    end_date = datetime.fromisoformat(request.form['end_date'])
    body = request.form['body']
    place = request.form['place']
    new_task = Interview(title=title, start_date=start_date, end_date=end_date, body=body, place=place)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/add_meeting', methods=['POST'])
def add_meeting():
    title = request.form['title']
    start_date = datetime.fromisoformat(request.form['start_date'])
    end_date = datetime.fromisoformat(request.form['end_date'])
    body = request.form['body']
    place = request.form['place']
    new_task = Meeting(title=title, start_date=start_date, end_date=end_date, body=body, place=place)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/add_intern', methods=['POST'])
def add_intern():
    title = request.form.get('title')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    body = request.form.get('body')
    place = request.form.get('place')
    # 文字列をdatetimeオブジェクトに変換
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    new_intern = Intern(title=title, start_date=start_date, end_date=end_date, body=body, place=place)
    db.session.add(new_intern)
    db.session.commit()
    return redirect('/')

@app.route('/delete/task/<int:task_id>',methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:  # オブジェクトが存在するかチェック
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    return 'Task not found', 404 

@app.route('/delete/interview/<int:interview_id>',methods=['POST'])
def delete_interview(interview_id):
    interview = Interview.query.get(interview_id)
    if interview:  # オブジェクトが存在するかチェック
        db.session.delete(interview)
        db.session.commit()
        return redirect('/')
    return 'Interview not found', 404

@app.route('/delete/meeting/<int:meeting_id>',methods=['POST'])
def delete_meeting(meeting_id):
    meeting = Meeting.query.get(meeting_id)
    if meeting:  # オブジェクトが存在するかチェック
        db.session.delete(meeting)
        db.session.commit()
        return redirect('/')
    return 'Meeting not found', 404

@app.route('/delete/intern/<int:intern_id>',methods=['POST'])
def delete_intern(intern_id):
    intern = Intern.query.get(intern_id)
    if intern:  # オブジェクトが存在するかチェック
        db.session.delete(intern)
        db.session.commit()
        return redirect('/')
    return 'Intern not found', 404

if __name__ == '__main__':
    app.run(debug=True)
