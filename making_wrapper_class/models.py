from datetime import datetime
from config import db

class Studentdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    teacher = db.Column(db.String(200))

    def __repr__(self):
        return '<Task %r>' % self.id

class authusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String())
    token = db.Column(db.String(200), default=False)
    new_dt = db.Column(db.DateTime, default=datetime.now())

def delete_data(task):
    db.session.delete(task)


def add_data(task):
    db.session.add(task)


def commit_changes():
    db.session.commit()