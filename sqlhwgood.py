from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import SearchForm, EditForm, NewUserForm, DeleteUserForm
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    footsize = db.Column(db.Integer)

@app.route('/',  methods = ['GET','POST'])
@app.route('/home',  methods = ['GET','POST'])
def home():

    searchform = SearchForm()
    if searchform.validate_on_submit():
        flash('Search requested for item {}'.format(
            searchform.search.data))
        return redirect('/searchuser/'+searchform.search.data)
    

    users = db.session.query(User).all()
    return render_template('home.html', title = 'Search', searchform=searchform, users=users)

@app.route('/newuser', methods = ['GET','POST'])
def adduser_page():
    searchform = SearchForm()
    if searchform.validate_on_submit():
        flash('Search requested for item {}'.format(
            searchform.search.data))
        return redirect('/searchuser/'+searchform.search.data)

    form = NewUserForm()
    if form.validate_on_submit():
        flash('New user instance requested for\nfname:{}\nlname:{}\nfootsize:{}'
            .format(form.fname.data,form.lname.data,form.footsize.data))
        user = User(fname=form.fname.data, lname=form.lname.data, footsize=form.footsize.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/searchuser/'+str(user.id))

    return render_template('newuser.html',title= 'NewUser', searchform=searchform,form=form)

@app.route('/searchuser/<personal_user>', methods=['GET','POST'])
def searchuser_page(personal_user):

    searchform = SearchForm()
    if searchform.validate_on_submit():
        flash('Search requested for item {}'.format(
            searchform.search.data))
        return redirect('/searchuser/'+searchform.search.data)

    users = User.query.filter_by(fname=personal_user).all()
    if users == []:
        users = User.query.filter_by(lname=personal_user).all()

    if users == []:
        users = User.query.filter_by(id=personal_user)  
    print(users)

    if users != []:
        print(users)
        return render_template('user.html', users=users, title='Search: '+personal_user, searchform= searchform)
    else:
        return('<h1>Error 404: No Users Found Under:<h1><h3>'+
        str(personal_user)+
        '<h3>' )

@app.route('/edit/<id>',  methods = ['GET','POST'])
def edit_page(id):

    searchform = SearchForm()
    if searchform.validate_on_submit():
        flash('Search requested for item {}'.format(
            searchform.search.data))
        return redirect('/searchuser/'+searchform.search.data)
    
    user = User.query.get(id)
    form = EditForm(fname = user.fname, lname = user.lname, footsize = user.footsize)
    
    if form.validate_on_submit():
        flash('Edit requested for items {}, {}, {}'.format(
            form.fname.data,
            form.lname.data,
            form.footsize.data))
        user.fname = form.fname.data
        user.lname = form.lname.data
        user.footsize = form.footsize.data
        db.session.commit()
        return redirect('/searchuser/'+str(user.id))
    
    return render_template(
        'edit.html', title = 'Edit ', user = user, form = form, searchform= searchform)


@app.route('/delete/<id>')
def deletepage(id):
    user = User.query.get(id)
    db.session.delete(user)
    return redirect('/home')

if __name__ == '__main__':
    app.run(debug=True)