from flask import render_template, url_for, redirect, flash, session
from app import app, db, models
from .models import Reader, Book
from .forms import ReaderForm, BookForm
import datetime


@app.route("/")
def homepage():
    # form = ReaderForm()
    # if form.validate_on_submit():
    #     tmp = models.Reader(name=form.name.data,password=form.password.data)
    #     db.session.add(tmp)
    #     db.session.commit()
    #     return redirect('/login') #display due tasks after user communityd a new task
     return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login(): #filter out all uncompleted tasks and display
    form = ReaderForm()
    if form.validate_on_submit():
        tmp = Reader(name=form.name.data,password=form.password.data)
        rdr = Reader.query.filter_by(name=tmp.name).first()
        if (tmp.password==rdr.password):
            session['active_user'] = form.name.data
            return redirect('/library')
        else:
            flash("Wrong information!")
    return render_template('login.html',
                        title="Sign in",form=form)

@app.route('/register',methods=['GET','POST'])
def register(): #filter out all uncompleted tasks and display
    form = ReaderForm()
    if form.validate_on_submit():
        tmp = models.Reader(name=form.name.data,password=form.password.data)
        db.session.add(tmp)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html',
                        title="Sign up",form=form)

@app.route('/library',methods=['GET','POST'])
def library():
    form = BookForm()
    if form.validate_on_submit():
        tmp = Book(title=form.title.data,description=form.description.data)
        db.session.add(tmp)
        db.session.commit()
        return redirect('/library')
    rdr = Reader.query.filter_by(name=session['active_user']).first()
    read_books = rdr.book
    books = Book.query.all()
    for book in read_books:
        books.remove(book)
    return render_template('library.html',books=books,form=form)

@app.route('/repo',methods=['GET','POST'])
def repo():
    form = ReaderForm()
    if form.validate_on_submit():
        tmp = Reader(password=form.password.data)
        rdr = Reader.query.filter_by(name=session['active_user']).first()
        rdr.password = tmp.password
        db.session.commit()
        return redirect('/library')
    rdr = Reader.query.filter_by(name=session['active_user']).first()
    books = rdr.book
    return render_template('repo.html',books=books,form=form)

@app.route('/unfinish/<id>') #agent route for tagging tasks as completed
def unfinish(id):
    rdr = Reader.query.filter_by(name=session['active_user']).first()
    tmp = Book.query.get(id)
    rdr.book.remove(tmp)
    db.session.commit()
    return redirect('/library') #display completed tasks after user tagged a task as completed

@app.route('/finish/<id>') #agent route for tagging tasks as completed
def finish(id):
    rdr = Reader.query.filter_by(name=session['active_user']).first()
    tmp = Book.query.get(id)
    rdr.book.append(tmp)
    db.session.commit()
    return redirect('/repo') #display completed tasks after user tagged a task as completed

@app.route('/logout')
def logout():
	session.pop('variable', None)
	return redirect('/login')

# @app.route('/community', methods=['GET', 'POST'])
# def community():
#     task = models.Task.query.filter_by(completed=False).all()
#     form = ReaderForm()
#     if form.validate_on_submit():
#         tmp = models.Task(title=form.title.data,description=form.description.data)
#         db.session.add(tmp)
#         db.session.commit()
#         return redirect(url_for('.login')) #display due tasks after user communityd a new task
#     return render_template('login.html',form=form,task=task)
