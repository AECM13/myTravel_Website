from flask import Flask, Blueprint, render_template, request, redirect,session,url_for,flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed
from werkzeug import secure_filename
from flask_login import login_user, logout_user, current_user , login_required
from dbUtils import user
import dbUtils
import os

UPLOADED_IMAGE_DEST = os.path.join('static','images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

listing_bp = Blueprint('listing_bp',__name__)


@listing_bp.route('/dashboard_user/places',methods=['GET', 'POST'])
@login_required
def add_new_place():
    if request.method == 'GET':
        return render_template('new_place.html')
    user_id = current_user.user_id
    place_name = request.form['place_name']
    place_address = request.form['place_address']
    place_website = request.form['place_website']
    place_phone = request.form['place_phone']
    place_description = request.form['place_description']
    place_picture = request.files['place_pic']
    if place_picture.filename == '':
        flash('No selected file')
        print('No selected file')
        return redirect(request.url)
    if place_picture and allowed_file(place_picture.filename):
        filename = secure_filename(place_picture.filename)
        print(filename)
        place_picture.save(os.path.join(UPLOADED_IMAGE_DEST, filename))
        dbUtils.new_place(user_id,place_name,place_address,place_website,place_phone,filename,place_description)
        flash('file uploaded successfully')
        return redirect(url_for('listing_bp.add_new_place'))
    else:
        return 'file did not uploaded successfully'

@listing_bp.route('/dashboard_user/user_post',methods=['GET', 'POST'])
@login_required
def show_user_places():
    username1 = 'Visitor'
    try:
        log_user = dbUtils.get_user(current_user.user_id)
        username1 = log_user
    except:
        username1 = 'Visitor'
    user_id = current_user.user_id
    data = dbUtils.get_place_by_user(user_id)
    profile_pic =[]
    for p in data:
        pic = p[6]
        pic_url = 'images/'+ pic
        js_dic ={"place_id":p[0],"pic_url":pic_url,"name":p[2],"address":p[3],"website":p[4],"phone_number":p[5],"description":p[7],"date_posted":p[8]}
        profile_pic.append(js_dic)
    return render_template('user_listing.html', data = data, profile_pic = profile_pic,username=username1)

@listing_bp.route('/dashboard_user/admin',methods=['GET', 'POST'])
@login_required
def admin_dash():
    username = dbUtils.get_user(current_user.user_id)
    check_admin = dbUtils.get_by_username(username)[4]
    if check_admin == 1:
        return 'admin pageeee'
    else:
        return 'Not allowed You aren\'t admin'




@listing_bp.route('/delete',methods=['POST'])
def delete():
    id_delete = request.form['delete']
    data = dbUtils.get_all_place_review(id_delete)
    if len(data) > 0:
        dbUtils.delete_review(id_delete)
    dbUtils.delete_place(id_delete)
    return redirect(url_for('listing_bp.show_user_places'))


@listing_bp.route('/all_listing', methods=['GET'])
def show_all_places():
    data = dbUtils.get_all_places()
    profile_pic =[]
    for p in data:
        pic = p[6]
        username = dbUtils.get_user(p[1])
        pic_url = 'images/'+ pic
        js_dic ={"place_id":p[0],"pic_url":pic_url,"name":p[2],"username":username,"address":p[3],"website":p[4],"phone_number":p[5],"description":p[7],"date_posted":p[8]}
        profile_pic.append(js_dic)
    username1 = 'Visitor'
    try:
        log_user = dbUtils.get_user(current_user.user_id)
        username1 = log_user
    except:
        username1 = 'Visitor'
    return render_template('search_results.html',username=username1, profile_pic=profile_pic)

@listing_bp.route('/all_listing/<place_id>', methods=['GET','POST'])
def show_selected_place(place_id):
    data = dbUtils.get_place_by_id(place_id)
    all_review = dbUtils.get_all_place_review(place_id)
    page_rev = []
    for p in all_review:
        user_name = dbUtils.get_user(p[2])
        date_review = p[3]
        rating = p[6]
        review = p[4]
        js_rev = {"username":user_name, "date_review":date_review, "rating":rating, "review":review}
        page_rev.append(js_rev)
    pic = data[6]
    username = dbUtils.get_user(data[1])
    pic_url = 'images/'+ pic
    js_dic ={"place_id":data[0],"pic_url":pic_url,"name":data[2],"username":username,"address":data[3],"website":data[4],"phone_number":data[5],"description":data[7],"date_posted":data[8]}
    username1 = 'Visitor'
    try:
        log_user = dbUtils.get_user(current_user.user_id)
        username1 = log_user
    except:
        username1 = 'Visitor'
    return render_template('place_list.html',username=username1, profile_pic = js_dic, place_rev = page_rev)
