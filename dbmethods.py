from flask import redirect
from sqlalchemy.orm import sessionmaker
from constants import *
import random
import string

def updateComment(task, new_comment, db):
    if task.comment == new_comment:
        return 0
    else:
        task.comment = new_comment
        db.session.commit()

def deleteTask(task_to_delete, db):
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except:
        return "error"

def checkIfExists(username, Users):
    i = 0
    try:
        while True:
            if Users.query.get_or_404(i).username == username:
                return True
            else:
                i += 1
    except:
        return False

def addTask(task, db):
    try:
        db.session.add(task)
        db.session.commit()
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

def moveTask(task, db, Todo, inProcess, Done):
    try:
        deleteTask(task, db)
        nextTable = getNextTable(task.modelClass, inProcess, Done)
        new_task = nextTable(content=task.content, comment=task.comment, owner=task.owner, date_created=task.date_created)
        addTask(new_task, db)
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

def randomString(stringLenght=24):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(stringLenght))

# ?
# def getId(username, Users):
#     i = 0
#     while True:
#         if Users.query.get_or_404(i).username == username:
#             return Users.query.get_or_404(i).uniqueId
#         else:
#             i += 1