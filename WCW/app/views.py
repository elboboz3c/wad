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
        if (rdr is not None and tmp.password==rdr.password):
            session['active_user'] = form.name.data
            return redirect('/library')
        else:
            flash("Wrong user name or password!")
    return render_template('login.html',
                        title="Sign in",form=form)

@app.route('/register',methods=['GET','POST'])
def register(): #filter out all uncompleted tasks and display
    form = ReaderForm()
    if form.validate_on_submit():
        tmp = models.Reader(name=form.name.data,password=form.password.data)
        user_existence = Reader.query.filter_by(name=tmp.name).first()
        if user_existence is None:
            db.session.add(tmp)
            db.session.commit()
            flash("Successfully created a new account, please log in!")
            return redirect('/login')
        else:
            flash("User already exists!")
    return render_template('register.html',
                        title="Sign up",form=form)

@app.route('/library',methods=['GET','POST'])
def library():
    rdr = Reader.query.filter_by(name=session['active_user']).first()
    read_books = rdr.book
    books = Book.query.all()
    for book in read_books:
        books.remove(book)
    return render_template('library.html',title="Book Library",books=books)

@app.route('/list',methods=['GET','POST'])
def list():
    book_form = BookForm()
    if book_form.validate_on_submit():
        tmp = Book(title=book_form.title.data,description=book_form.description.data)
        book_existence = Book.query.filter_by(title=tmp.title).first()
        if book_existence is None:
            rdr = Reader.query.filter_by(name=session['active_user']).first()
            tmp.reader.append(rdr)
            db.session.add(tmp)
            db.session.commit()
            flash("Successfully added a book to your list!")
            return redirect('/list')
        else:
            flash("Book already exists!")
    password_form = ReaderForm()
    if password_form.validate_on_submit():
        # tmp = Reader(password=form.password.data)
        rdr = Reader.query.filter_by(name=session['active_user']).first()
        rdr.password = password_form.password.data
        db.session.commit()
        flash("Your password is successfully changed!")
        return redirect('/list')
    rdr = Reader.query.filter_by(name=session['active_user']).first()
    books = rdr.book
    return render_template('list.html',title="Personal book list",books=books,book_form=book_form,password_form=password_form)

@app.route('/unfinish/<id>') #agent route for tagging tasks as completed
def unfinish(id):
    rdr = Reader.query.filter_by(name=session['active_user']).first()
    tmp = Book.query.get(id)
    rdr.book.remove(tmp)
    db.session.commit()
    flash("Successfully deleted from your list!")
    return redirect('/list') #display completed tasks after user tagged a task as completed

@app.route('/finish/<id>') #agent route for tagging tasks as completed
def finish(id):
    rdr = Reader.query.filter_by(name=session['active_user']).first()
    tmp = Book.query.get(id)
    rdr.book.append(tmp)
    db.session.commit()
    flash("Successfully added a book to your list!")
    return redirect('/library') #display completed tasks after user tagged a task as completed

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
