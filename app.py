from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import dataBase
from dbmethods import deleteTask
from dbmethods import moveTask
import uuid
from dbmethods import getTask, checkAccess
from constants import *
import os
from sqlalchemy.orm import sessionmaker
from flask import session

# Todo: create pages with their own Dodo's
# TODO: error handling
# TODO: Login
# ALSO create sign up, sql table for usernames and passwords and list with indexses for todo`s

# sqllite database
app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_CFG
db = dataBase.data(app)
# табличка, яка зберігає значення, які вводить юзер 
class Todo(db.Model):
    modelClass = db.Column(db.Integer, default=TODO_MODEL_NUMBER)
    id = db.Column(db.Integer, primary_key=True)
    # nullable, тому що контент не може бути пустий
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String, default="")

    def __repl__(self):
        return "<Task %s>" % self.id

# табличка, яка приймає значення, які переходять з ToDo в In process
class inProcess(db.Model):
    modelClass = db.Column(db.Integer, default=INPROCESS_MODEL_NUMBER)
    id = db.Column(db.Integer, primary_key=True)
    # nullable відсутній, адже є в ToDo
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String, default="")

    def __repl__(self):
        return "<Task %s>" % self.id

# табличка, яка приймає значення, які переходять з ToDo в In process
class Done(db.Model):
    modelClass = db.Column(db.Integer, default=DONE_MODEL_NUMBER)
    id = db.Column(db.Integer, primary_key=True)
    # nullable відсутній, адже є в ToDo
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String, default="")

    def __repl__(self):
        return "<Task %s>" % self.id

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __repl__(self):
        return "<User %s>" % self.id

# Main page
@app.route('/', methods=["POST", "GET"])
def index():
    if session.get('logged_in'):
        if request.method == "POST":
            task_content = request.form['content']
            new_task = Todo(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect("/")
            except:
                return "error"
        else:   
            tasks = Todo.query.order_by(Todo.date_created).all()
            process = inProcess.query.order_by(inProcess.date_created).all()
            done = Done.query.order_by(Done.date_created).all()
            return render_template('index.html', tasks=tasks, process=process, done=done)
    else:
        return redirect("/login")

@app.route("/move/<int:modelClass>/<int:id>")
def move(modelClass, id):
    if session.get('logged_in'):
        return moveTask(modelClass, id, db, Todo, inProcess, Done)
    else:
        return redirect("/login")

@app.route('/delete/<int:modelClass>/<int:id>', methods=["POST", "GET"])
def delete(modelClass, id):
    if session.get('logged_in'):
        task = getTask(modelClass, id, Todo, inProcess, Done)
        return deleteTask(task, db)
    else:
        return redirect("/login")

@app.route('/comment/<int:modelClass>/<int:id>', methods=["POST", "GET"])
def commentary(modelClass, id):
    if session.get('logged_in'):
        task = getTask(modelClass, id, Todo, inProcess, Done)

        if request.method == "POST":
            task.comment = request.form["comment"]
            try:
                db.session.commit()
                return redirect("/")
            except:
                return "error"
        else:
            return render_template("comment.html", task=task)
    else:
        return redirect("/login")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if checkAccess(request.form["password"], request.form["username"], Users):
            session["logged_in"] = True
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect("/login")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)  