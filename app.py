from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import dataBase

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

db = dataBase.data(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repl__(self):
        return "<Task %s>" % self.id


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
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    taks_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taks_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "error"

@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "error"
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)  