from app import db
import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) #id is not presented to the user, but is used to identify tasks at the backend
    title = db.Column(db.String(500))
    description = db.Column(db.String(1000))
    date = db.Column(db.DateTime,default=datetime.datetime.utcnow()) #store the date automatically
    completed = db.Column(db.Boolean,default=False) #tag that indicates whether a task is completed
