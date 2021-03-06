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

# ================================ [ TODOs ] ===================================================

# TODO: ?? create pages with their own Dodo's ??
# TODO: error handling
# TODO: register via email

# ================================ [ TODOs ] ===================================================
# ==============================================================================================

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = dataBase.data(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.secret_key = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERROR)

# ==============================================================================================
# ================================ [ Models for db ] ===========================================

class Todo(db.Model):
    modelClass = db.Column(db.Integer, default=TODO_MODEL_NUMBER)
    id = db.Column(db.Integer, primary_key=True)
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
    date_created = db.Column(db.DateTime)
    comment = db.Column(db.String, default="")
    owner = db.Column(db.String)

    def __repl__(self):
        return "<Task %s>" % self.id

class Done(db.Model):
    modelClass = db.Column(db.Integer, default=DONE_MODEL_NUMBER)
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime)
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

# ================================ [ Models for db ] =============================================
# ================================================================================================
# ================================= [ Index page ] ===============================================

@app.route('/', methods=["POST", "GET"])
def index():    
    current_user = str(session.get("user"))
    if session.get('logged_in'):
        session["logged_in"] = True
        session["user"] = current_user
        if request.method == "POST":
            if request.form["content"] != "":
                task_content = request.form['content']
                new_task = Todo(content=task_content, owner=current_user)
                addTask(new_task, db)
            return redirect("/")
        else:   
            tasks = Todo.query.filter_by(owner=current_user).all()
            process = inProcess.query.filter_by(owner=current_user).all()
            done = Done.query.filter_by(owner=current_user).all()
            return render_template('index.html', tasks=tasks, process=process, done=done)
    
    else:
        return redirect("/login")

# ================================= [ Index page ] ===============================================
# ==================================================================================================
# ================================= [ Moving url ] =================================================

@app.route("/move/<int:modelClass>/<int:id>")
def move(modelClass, id):
    if session.get('logged_in'):
        session["logged_in"] = True
        task = getTask(modelClass, id, Todo, inProcess, Done)
        if checkOwner(session.get('user'), task.owner):
            session["user"] = session.get('user')
            moveTask(task, db, Todo, inProcess, Done)
    return redirect("/")

# ================================= [ Moving url ] =================================================
# ==================================================================================================
# ================================= [ Delete url ] =================================================

@app.route('/delete/<int:modelClass>/<int:id>', methods=["POST", "GET"])
def delete(modelClass, id):
    if session.get('logged_in'):
        session["logged_in"] = True
        task = getTask(modelClass, id, Todo, inProcess, Done)
        if checkOwner(session.get('user'), task.owner):
            session["user"] = session.get('user')
            deleteTask(task, db)
    return redirect("/")

# ================================= [ Delete url ] =================================================
# ==================================================================================================
# ================================= [ Comment url ] ================================================
@app.route('/comment/<int:modelClass>/<int:id>', methods=["POST", "GET"])
def commentary(modelClass, id):
    if session.get('logged_in'):
        session["logged_in"] = True
        task = getTask(modelClass, id, Todo, inProcess, Done)
        if checkOwner(session.get('user'), task.owner):
            session["user"] = session.get('user')
            if request.method == "POST":
                updateComment(task, request.form["comment"], db)
                return redirect("/")
            else:
                return render_template("comment.html", task=task)
    return redirect("/")

# ================================= [ Comment url ] ================================================
# ==================================================================================================
# ================================= [ Login url ] ==================================================

@app.route('/login', methods=["POST", "GET"])
def login():
    error = session.get("error")

    if error == "Username is already taken. Try something different":
        session["error"] = None
        error = None

    session["logged_in"] = False
    session["user"] = None
    if request.method == "POST":
        if checkAccess(request.form["password"], request.form["username"], Users.query.all()):
            session["logged_in"] = True
            session["user"] = request.form["username"]
            session["error"] = None
            return redirect("/")
        else:
            session["error"] = "Invalid username or password. Try again"
            return redirect("/login")
    else:
        return render_template('login.html', error=error)

# ================================= [ Login url ] ==================================================
# ==================================================================================================
# ================================= [ Register url ] ===============================================

@app.route("/register", methods=["POST", "GET"])
def logout():
    error = session.get("error")

    if error == "Invalid username or password. Try again":
        session["error"] = None
        error = None

    if request.method == "POST":
        if request.form["username"] != "" and request.form["password"] != "":
            # check if username is taken
            if not inDB(Users, request.form["username"].lower()): 
                addTask(Users(username=str(request.form["username"]).lower(), password=request.form["password"], uniqueId=randomString()), db)
                session["logged_in"] = True
                session["error"] = None   
            else:
                session["error"] = "Username is already taken. Try something different"
                return redirect("/register")
        return redirect("/login")
    else:
        return render_template("register.html", error=error)

# ================================= [ Register url ] ===============================================

if __name__ == "__main__":
    app.run()  