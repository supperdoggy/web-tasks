from flask_sqlalchemy import SQLAlchemy


def data(application):
    db = SQLAlchemy(app=application)
    return db