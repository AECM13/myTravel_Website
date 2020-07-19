from flask import Flask, Blueprint, render_template, request, redirect,session
from flask_login import login_user, logout_user, current_user , login_required
import dbUtils
from dbUtils import user

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard_user',methods=['GET'])
@login_required
def user_dashboard():
    username = dbUtils.get_user(current_user.user_id)
    admin = dbUtils.get_by_username(username)[4]
    return render_template('dashboard_user.html',username = username, admin = admin)
