from flask import redirect
from sqlalchemy.orm import sessionmaker
from constants import *

def deleteTask(task_to_delete, db):
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "error"

def getTable(modelId, Todo, inProcces, Done):
    if modelId == TODO_MODEL_NUMBER:
        return Todo
    
    elif modelId == INPROCESS_MODEL_NUMBER:
        return inProcces
    
    elif modelId == DONE_MODEL_NUMBER:
        return Done

def getNextTable(modelId, inProcces, Done):
    if modelId == TODO_MODEL_NUMBER:
        return inProcces
    elif modelId == INPROCESS_MODEL_NUMBER:
        return Done

def moveTask(modelId, id, db, Todo, inProcess, Done):
    table = getTable(modelId, Todo, inProcess, Done)
    task_to_move = table.query.get_or_404(id)

    try:
        db.session.delete(task_to_move)
        db.session.commit()

        nextTable = getNextTable(modelId, inProcess, Done)
        new_task = nextTable(content=task_to_move.content, comment=task_to_move.comment)
    
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    except:
        return "error"

def getTask(modelId, id, Todo, inProcess, Done):
    if modelId == TODO_MODEL_NUMBER:
        task = Todo.query.get_or_404(id)
    elif modelId == INPROCESS_MODEL_NUMBER:
        task = inProcess.query.get_or_404(id)
    elif modelId == DONE_MODEL_NUMBER:
        task = Done.query.get_or_404(id)
    
    return task

def checkAccess(password, username,Users):
    i = 1
    try:
        while True:
            if Users.query.get_or_404(i).username == username and  Users.query.get_or_404(i).password == password:
                return True
            else:
                i += 1
    except:
        return False
