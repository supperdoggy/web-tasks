from flask import redirect


def deleteTask(table, id, db):
    taks_to_delete = table.query.get_or_404(id)
    try:
        db.session.delete(taks_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "error"

def move(table, nextTable, id, db):

    task_to_move = table.query.get_or_404(id)

    try:
        db.session.delete(task_to_move)
        db.session.commit()
        
        new_task = nextTable(content=task_to_move.content)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    except:
        return "error"