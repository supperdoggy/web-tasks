### Автор 
## Марчишак Максим Арсенович ІПЗ-13

Індивідуальна робота "Todo"

## Короткий опис программи
Веб программа (backend, frontend), яка допомагає відслідковувати та додавати заплановані цілі, робити нотатки до цілей.Присутня система авторизації та автентифікації. Задеплоїна на хероку, доступна за посиланням: simple-web-tasks.herokuapp.com. 

Посилання на github: https://github.com/supperdoggy/web-tasks

## Використані технології
Backend: python3, flask, flask-login, sqlalchemy

Fronend: html, css, js

База даних: postgres

# Принцип роботи
В базі данних присутні 4 моделі: Users - модель з інформацією про користувачів, Todo - модель для запланованих справ, inProcess - модель для справ, які в процесі виконання і Done - модель для виконаних справ. Також присутнє шифрування данних cookie для того щоб забезпечити захист інформації. 

Налаштування

```python
# Оголошуємо перемінну app та даємо посилання на папку з html
app = Flask(__name__, template_folder="templates")
# Підключаємо базу даних
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# Оголошуємо базу даних
db = dataBase.data(app)
# Підключаємо login_manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Оголошуємо ключ шифрування
app.secret_key = secret_key

app.config['SESSION_TYPE'] = 'filesystem'
```

Посиланяння "/" відповідає за основну сторінку. На ній відображені справи конкретно цього користувача
``` python
@app.route('/', methods=["POST", "GET"])
def index():    
    # Отримуємо поточного користувача
    current_user = str(session.get("user"))
    # Якщо здійснено авторизацію, то допускається робота з програмою
    if session.get('logged_in'):
        # Якщо метод POST, то додаємо нову заплановану справу
        if request.method == "POST":
            # Якщо поле пусте, то нічого не змінюється
            if request.form["content"] != "":
                # додаємо нову справу в базу данних
                task_content = request.form['content']
                new_task = Todo(content=task_content, owner=current_user)
                addTask(new_task, db)
            # оновлюємо сторінку
            return redirect("/")
        # Якщо метод не POST
        else:
            tasks = Todo.query.filter_by(owner=current_user).all()
            process = inProcess.query.filter_by(owner=current_user).all()
            done = Done.query.filter_by(owner=current_user).all()
            # Повертаємо оброблений html з справами
            return render_template('index.html', tasks=tasks, process=process, done=done)
    # Якщо не здійснено авторизацію, то повертає на сторінку авторизації
    else:
        return redirect("/login")
```

Посилання "/delete" відповідає за видалення конкретної справи

```python
@app.route('/delete/<int:modelClass>/<int:id>', methods=["POST", "GET"])
def delete(modelClass, id):
    # Якщо здійснено авторизацію, то допускається робота з програмою
    if session.get('logged_in'):
        # отримуємо справу
        task = getTask(modelClass, id, Todo, inProcess, Done)
        # Перевіряємо чи власник справи збігається з поточним
        if checkOwner(session.get('user'), task.owner):
            # Видаляємо справу
            deleteTask(task, db)
    # Повертаємо на головну сторінку
    return redirect("/")
```

Посилання "/comment" відповідає за додавання нотаток до справи

```python
@app.route('/comment/<int:modelClass>/<int:id>', methods=["POST", "GET"])
def commentary(modelClass, id):
    # Якщо здійснено авторизацію, то допускається робота з програмою
    if session.get('logged_in'):
        # отримуємо справу
        task = getTask(modelClass, id, Todo, inProcess, Done)
        # Перевіряємо чи власник справи збігається з поточним
        if checkOwner(session.get('user'), task.owner):
            # Якщо метод POST, то оновляємо коментарі
            if request.method == "POST":
                # Оновляємо коментарі
                updateComment(task, request.form["comment"], db)
                # Повертаємося на гловну сторінку
                return redirect("/")
            else:
                # Рендеримо html для коментарів
                return render_template("comment.html", task=task)
    # Повертаємося на головну сторінку 
    return redirect("/")
```

Посилання "/login" відповідає за авторизацію користувача

```python
@app.route('/login', methods=["POST", "GET"])
def login():
    # Скидаємо cookie
    session["logged_in"] = False
    session["user"] = None
    # Якщо метод POST, то перевіряємо чи є такий користувач
    if request.method == "POST":
        # Якщо True
        if checkAccess(request.form["password"], request.form["username"], Users.query.all()):
            # оноволюємо cookie
            session["logged_in"] = True
            session["user"] = request.form["username"]
            # Повертаємось на головну сторінку
            return redirect("/")
        else:
            # Якщо дані не збігаються то повертаємося знову на посилання login
            return redirect("/login")
    else:
        # Рендеримо login.html
        return render_template('login.html')
```