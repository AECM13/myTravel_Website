from flask import Flask, Blueprint, render_template, request, redirect, flash
from ..databaseconn.dbUtils import user
import ..databaseconn.dbUtil
from flask_login import login_user, logout_user, current_user , login_required
from werkzeug.security import check_password_hash, generate_password_hash

reg_bp = Blueprint('reg_bp', __name__)

@reg_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        print(2)
        email = request.form['email_name_new']
        username = request.form['user_name_new']
        password = request.form['pwd_new']
        very_password = request.form['ver_pwd']
        hash_password = generate_password_hash(password)
        print(email)
        print(hash_password)
        dbUtils.signup(username, email, hash_password)
        flash('Username already registered. Please try again')
        print('Username already registered. Please try again')
        return redirect('/login')
    else:
        return render_template('signup.html')

@reg_bp.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['user_name']
        password = request.form['pwd']
        print(username)
        print(password)
        check_user = dbUtils.login(username)
        print(check_user)
        if check_user == None:
            flash("Username is invalid", 'error')
            print("Username is invalid")
            return redirect('/login')
        pass_hashed = check_user[3]
        print(check_password_hash(pass_hashed, password))
        if not check_password_hash(pass_hashed, password):
            flash("Password is invalid", 'error')
            print("Password is invalid")
            return redirect('/login')
        user_logged = user(check_user[0])
        login_user(user_logged)
        flash("Logged in successfully")
        return redirect('/')


@reg_bp.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')
