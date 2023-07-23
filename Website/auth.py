from flask import Blueprint, render_template, request, flash, redirect,url_for
from .models import *
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth', __name__)

@auth.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login success', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password!', category= 'error')
        else:
            flash('Invalid Username.', category ='error' )
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods = ['POST','GET']) 
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        user_name = User.query.filter_by(username = username).first()
        if user:
            flash('Account already exist',category="error")
        elif user_name:
            flash('This username has been taken by someone before please choose another one.')
        elif(len(email)<2):
            flash("Email must be at least two characters long",category = 'error')
        elif(len(fullname)<3):
            flash("Full name should have more than three letters.", category = 'error')
        elif len(username) < 3:
            flash("Username is too short!", category = 'error')
        elif len(password) < 3:
            flash("Password needs to contain minimum of four digits and alphabets only!", category = 'error')
        else:
            new_user = User(email = email,name = fullname,username = username, password = generate_password_hash(password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account Created", category = 'success')
            #redirect user back home page after registration successfull!
            return redirect(url_for('views.home'))


    return render_template('signup.html')