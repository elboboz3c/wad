from flask import render_template, url_for, redirect
from app import app, db, models
from .forms import CreateForm
import datetime


@app.route('/')
def cora(): #filter out all uncompleted tasks and display
    task = models.Task.query.filter_by(completed=False).all()
    return render_template('/cora.html',
                       task=task)

@app.route('/resource')
def resource(): #filter out all completed tasks and display
    task = models.Task.query.filter_by(completed=True).all()
    return render_template('/resource.html',
                       task=task)

@app.route('/community', methods=['GET', 'POST'])
def community():
    task = models.Task.query.filter_by(completed=False).all()
    form = CreateForm()
    if form.validate_on_submit():
        tmp = models.Task(title=form.title.data,description=form.description.data)
        db.session.add(tmp)
        db.session.commit()
        return redirect(url_for('.community')) #display due tasks after user communityd a new task
    return render_template('/community.html',form=form,task=task)

@app.route('/toComplete/<temp>') #agent route for tagging tasks as completed
def toComplete(temp):
    tmp = models.Task.query.get(temp)
    tmp.completed = 1
    db.session.commit()
    return redirect(url_for('.community')) #display completed tasks after user tagged a task as completed
