from app import db
import datetime

readship = db.Table('readship', db.Model.metadata,
    db.Column('readerId', db.Integer, db.ForeignKey('reader.id')),
    db.Column('bookId', db.Integer, db.ForeignKey('book.id'))
)

class Reader (db.Model):
    id = db.Column(db.Integer, primary_key=True) #id is not presented to the user, but is used to identify tasks at the backend
    name = db.Column(db.String(250), index=True)
    password = db.Column(db.String(250),index=True)
    book = db.relationship('Book',secondary=readship)
    def __repr__(self):
        return  self.name

class Book (db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250), index=True)
    reader = db.relationship('Reader',secondary=readship)
    def __repr__(self):
        return  self.title
