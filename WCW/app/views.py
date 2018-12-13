from flask import render_template, url_for, redirect
from app import app, db, models
from .forms import ReaderForm
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
        tmp = models.Reader(name=form.name.data,password=form.password.data)
        db.session.add(tmp)
        db.session.commit()
        return redirect('/login') #display due tasks after user communityd a new task
    return render_template('login.html',
                        title="Sign in",form=form)

@app.route('/register',methods=['GET','POST'])
def register(): #filter out all uncompleted tasks and display
    form = ReaderForm()
    if form.validate_on_submit():
        tmp = models.Reader(name=form.name.data,password=form.password.data)
        db.session.add(tmp)
        db.session.commit()
        return redirect('/login') #display due tasks after user communityd a new task
    return render_template('register.html',
                        title="Sign up",form=form)

@app.route('/resource')
def resource(): #filter out all completed tasks and display
    task = models.Task.query.filter_by(completed=True).all()
    return render_template('/resource.html',
                       task=task)

@app.route('/community', methods=['GET', 'POST'])
def community():
    task = models.Task.query.filter_by(completed=False).all()
    form = ReaderForm()
    if form.validate_on_submit():
        tmp = models.Task(title=form.title.data,description=form.description.data)
        db.session.add(tmp)
        db.session.commit()
        return redirect(url_for('.login')) #display due tasks after user communityd a new task
    return render_template('login.html',form=form,task=task)

@app.route('/toComplete/<temp>') #agent route for tagging tasks as completed
def toComplete(temp):
    tmp = models.Task.query.get(temp)
    tmp.completed = 1
    db.session.commit()
    return redirect(url_for('.login')) #display completed tasks after user tagged a task as completed
