from flask import Flask, Blueprint, render_template, request, redirect,session
from werkzeug.security import check_password_hash, generate_password_hash
import dbUtils
from dbUtils import user
from users import *
from flask_login import LoginManager, login_required, current_user


app = Flask(__name__)
app.secret_key ="saldfksadlfksfas;flvknadf"
app.register_blueprint(reg_bp)
@app.route('/')
def home():
    username = 'Visitor'
    return render_template("index.html", username = username)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
@login_manager.user_loader
def load_user(id):
    print(id)
    return user(id)


if __name__ == "__main__":
    app.debug = True
    app.run()
