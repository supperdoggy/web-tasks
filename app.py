from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import dataBase
from dbmethods import deleteTask
from dbmethods import moveTask


# sqllite database
app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = dataBase.data(app)

# табличка, яка зберігає значення, які вводить юзер 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable, тому що контент не може бути пустий
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repl__(self):
        return "<Task %s>" % self.id

# табличка, яка приймає значення, які переходять з ToDo в In process
class inProcess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable відсутній, адже є в ToDo
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repl__(self):
        return "<Task %s>" % self.id

# табличка, яка приймає значення, які переходять з ToDo в In process
class Done(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable відсутній, адже є в ToDo
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repl__(self):
        return "<Task %s>" % self.id

# Main page
@app.route('/', methods=["POST", "GET"])
def index():
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
        render_template("base.html")
        return render_template('index.html', tasks=tasks, process=process, done=done)

# route for deleting ToDo things
@app.route('/delete/<int:id>')
def delete(id):
    return deleteTask(Todo, id, db)

# moving to inProgress
@app.route("/inprogress/<int:id>", methods=["POST", "GET"])
def inprogress(id):
    return move(Todo, inProcess, id, db)

# deleting from inProgress
@app.route("/inprogress/delete/<int:id>", methods=["POST", "GET"])
def deleteTaskInProgress(id):
    return deleteTask(inProcess, id, db)

# moving to Done
@app.route('/done/<int:id>', methods=["POST", "GET"])
def moveToDone(id):
    return move(inProcess, Done, id, db)

# deliting from
@app.route("/done/delete/<int:id>", methods=["POST", "GET"])
def deleteDone(id):
    return deleteTask(Done, id, db)


if __name__ == "__main__":
    app.run(debug=True)  