from flask import Flask, Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user , login_required
from werkzeug.security import check_password_hash, generate_password_hash
from dbUtils import user
from validate_email import validate_email
import dbUtils


reg_bp = Blueprint('reg_bp', __name__)

@reg_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email_name_new']
        username = request.form['user_name_new']
        password = request.form['pwd_new']
        very_password = request.form['ver_pwd']
        is_valid = validate_email(email,check_mx=True)
        if is_valid:
            pass
        else:
            flash('Email is not valid please check if something wrong, try again')
            return redirect('/login')
        if password != very_password:
            flash('Password does not match. Please try again')
            return redirect('/login')
        if password == username:
            flash('Password cannot be the same as the username. Please try again')
            return redirect('/login')
        hash_password = generate_password_hash(password)
        if dbUtils.get_by_username(username) != None:
            flash('Username already registered. Please try again')
            return redirect('/login')
        if dbUtils.get_email(email) != None:
            flash('email already registered. Please log in ')
            return redirect('/login')
        flash("Sign up successfully, please log in")
        dbUtils.signup(username, email, hash_password)
        return redirect('/login')
    else:
        return render_template('login.html')

@reg_bp.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    elif request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['user_name']
        password = request.form['pwd']
        check_user = dbUtils.login(username)
        if check_user == None:
            flash("Username is invalid", 'error')
            return redirect('/login')
        pass_hashed = check_user[3]
        if not check_password_hash(pass_hashed, password):
            flash("Password is invalid", 'error')
            return redirect('/login')
        user_logged = user(check_user[0])
        login_user(user_logged)
        flash("Logged in successfully")
        return redirect('/')


@reg_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect('/')
