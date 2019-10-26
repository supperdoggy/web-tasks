from flask import redirect
from sqlalchemy.orm import sessionmaker
from random import randint
import random


def deleteTask(task_to_delete, db):
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "error"

def getTable(modelId, Todo, inProcces, Done):
    if modelId == 1:
        return Todo
    
    elif modelId == 2:
        return inProcces
    
    else:
        return Done

def getNextTable(modelId, inProcces, Done):
    if modelId == 1:
        return inProcces
    else:
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

def uniqueStrGenerator(self=24):
    low_letters = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                   'z', 'x', 'c', 'v', 'b', 'n', 'm']
    high_letters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                    'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    symbols = ['!', '@', '#', '$', '&', '?']
    pas_keys = low_letters + high_letters + nums + symbols
    random.shuffle(pas_keys)
    i = 0
    uniqueStr = ""
    while i < self:
        uniqueStr += pas_keys[0]
        pas_keys.remove(pas_keys[0])
        i += 1
    return uniqueStr

def getTask(modelId, id, Todo, inProcess, Done):
    if modelId == 1:
        task = Todo.query.get_or_404(id)
    elif modelId == 2:
        task = inProcess.query.get_or_404(id)
    else:
        task = Done.query.get_or_404(id)
    
    return task

    
