from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import dataBase
import uuid
from constants import *
import os
from sqlalchemy.orm import sessionmaker
from flask import session, g
from dbmethods import *
from uuid import uuid4
import flask_login

# Todo: create pages with their own Dodo's
# TODO: error handling
# TODO: register

# sqllite database
app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_CFG
db = dataBase.data(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class Todo(db.Model):
    modelClass = db.Column(db.Integer, default=TODO_MODEL_NUMBER)
    id = db.Column(db.Integer, primary_key=True)
    # nullable, тому що контент не може бути пустий
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String, default="")
    owner = db.Column(db.String)

    def __repl__(self):
        return "<Task %s>" % self.id

class inProcess(db.Model):
    modelClass = db.Column(db.Integer, default=INPROCESS_MODEL_NUMBER)
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String, default="")
    owner = db.Column(db.String)

    def __repl__(self):
        return "<Task %s>" % self.id

class Done(db.Model):
    modelClass = db.Column(db.Integer, default=DONE_MODEL_NUMBER)
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String, default="")
    owner = db.Column(db.String)

    def __repl__(self):
        return "<Task %s>" % self.id

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniqueId = db.Column(db.String, unique=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repl__(self):
        return "<User %s>" % self.id

# Main page
@app.route('/', methods=["POST", "GET"])
def index():    
    current_user = str(session.get("user"))
    if session.get('logged_in'):
        if request.method == "POST":
            if request.form["content"] != "":
                task_content = request.form['content']
                new_task = Todo(content=task_content, owner=current_user)
                addTask(new_task, db)

                return redirect("/")
            else:
                return redirect("/")
        else:   
            tasks = Todo.query.filter_by(owner=current_user).all()
            process = inProcess.query.filter_by(owner=current_user).all()
            done = Done.query.filter_by(owner=current_user).all()
            return render_template('index.html', tasks=tasks, process=process, done=done)
    
    else:
        return redirect("/login")

@app.route("/move/<int:modelClass>/<int:id>")
def move(modelClass, id):
    current_user = session.get("user")
    if session.get('logged_in'):
        return moveTask(modelClass, id, current_user, db, Todo, inProcess, Done)
    
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
            db.session.commit()
            return redirect("/")
        else:
            return render_template("comment.html", task=task)
    else:
        return redirect("/login")

@app.route('/login', methods=["POST", "GET"])
def login():
    session["logged_in"] = False
    session["user"] = None
    if request.method == "POST":
        if checkAccess(request.form["password"], request.form["username"], Users):
            session["logged_in"] = True
            session["user"] = request.form["username"]
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return render_template('login.html')

@app.route("/register", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        if request.form["username"] != "" and request.form["password"] != "":
            addTask(Users(username=request.form["username"], password=request.form["password"], uniqueId=randomString()), db)
            session["logged_in"] = True
            return redirect("/login")
        else:
            return redirect("/login")
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)  