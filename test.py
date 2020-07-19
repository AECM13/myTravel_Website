from flask import Flask, Blueprint, render_template, request, redirect,session,flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_required, current_user
import dbUtils
from dbUtils import user
from users import *
import os
from dashboard import *
from listing import *
from review import *
from send_email import send_email
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed



app = Flask(__name__)
app.secret_key ="saldfksadlfksfas;flvknadf"
app.register_blueprint(reg_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(listing_bp)
app.register_blueprint(review_bp)

@app.route('/', methods=['GET','POST'])
def home():
    username = 'Visitor'
    data = dbUtils.get_all_places()
    profile_pic =[]
    for p in data:
        pic = p[6]
        pic_url = 'images/'+ pic
        js_dic = {"pic_url":pic_url,"place_id":p[0]}
        profile_pic.append(js_dic)
    try:
        log_user = dbUtils.get_user(current_user.user_id)
        username = log_user
    except:
        username = 'Visitor'

    return render_template("index.html", username = username, profile_pic = profile_pic)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
@login_manager.user_loader
def load_user(id):
    return user(id)

UPLOADED_IMAGE_DEST = os.path.join('static','images')
#app.config['UPLOADED_IMAGE_DEST'] =UPLOADED_IMAGE_DEST

@app.route('/search_results', methods=['GET','POST'])
def search_results():
    username = 'Visitor'
    try:
        log_user = dbUtils.get_user(current_user.user_id)
        username = log_user
    except:
        username = 'Visitor'
    if request.method == 'POST':
        search = request.form['looking']
        profile_pic =[]
        try:
            p =dbUtils.get_place_by_name(search.title())
            pic = p[6]
            username = dbUtils.get_user(p[1])
            pic_url = 'images/'+ pic
            js_dic ={"place_id":p[0],"pic_url":pic_url,"name":p[2],"username":username,"address":p[3],"website":p[4],"phone_number":p[5],"description":p[7],"date_posted":p[8]}
            profile_pic.append(js_dic)
            return render_template('search_results.html', username=username, profile_pic=profile_pic)
        except:
            data =dbUtils.get_place_by_name1(search.title())
            if len(data) == 0:
                flash('place not found in website')
                return redirect('/')
            for p in data:
                pic = p[6]
                username = dbUtils.get_user(p[1])
                pic_url = 'images/'+ pic
                js_dic ={"place_id":p[0],"pic_url":pic_url,"name":p[2],"username":username,"address":p[3],"website":p[4],"phone_number":p[5],"description":p[7],"date_posted":p[8]}
                profile_pic.append(js_dic)
            return render_template('search_results.html', username=username, profile_pic=profile_pic)


    return render_template('search_results.html', username=username, profile_pic=profile_pic)

@app.route('/contact_me', methods=['GET','POST'])
def contact_me():
    username = 'Visitor'
    try:
        log_user = dbUtils.get_user(current_user.user_id)
        username = log_user
    except:
        username = 'Visitor'
    if request.method =='POST':
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        contact_message = request.form['contact_message']
        send_email(contact_email, contact_name, contact_message)
        return 'message send'
    else:
        return render_template("contact_me.html", username=username)

@app.route('/about', methods=['GET'])
def about_me():
    username = 'Visitor'
    try:
        log_user = dbUtils.get_user(current_user.user_id)
        username = log_user
    except:
        username = 'Visitor'
    return render_template("about.html", username=username)


app.config.from_object(__name__)
if __name__ == "__main__":
    app.debug = True
    app.run()
