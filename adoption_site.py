import os
from forms import AddForm , DelForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretket'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"Student name: {self.name}"

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add',methods=['GET','POST'])
def add_stud():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        new_stud = Student(name)
        db.session.add(new_stud)
        db.session.commit()
        return redirect(url_for('list_stud'))
    return render_template('add.html',form=form)


@app.route('/list')
def list_stud():
    students = Student.query.all()
    return render_template('list.html', students=students)

@app.route('/delete', methods=['GET', 'POST'])
def del_stud():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        stud = Student.query.get(id)
        db.session.delete(stud)
        db.session.commit()

        return redirect(url_for('list_stud'))
    return render_template('delete.html',form=form)