from flask import Flask, Blueprint, render_template, request, redirect,session,flash,url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed
from werkzeug import secure_filename
from flask_login import login_user, logout_user, current_user , login_required
from dbUtils import user
import dbUtils
import os

review_bp = Blueprint('review_bp',__name__)


@review_bp.route('/dashboard_user/all_reviews',methods=['GET', 'POST'])
@login_required
def all_reviews():
    username1 = 'Visitor'
    try:
        log_user = dbUtils.get_user(current_user.user_id)
        username1 = log_user
    except:
        username1 = 'Visitor'
    user_id = current_user.user_id
    data = dbUtils.get_review_by_user(user_id)
    data2 = dbUtils.get_all_place_user(user_id)
    review_dic = []
    my_rev = []
    for p in data:
        pic = dbUtils.get_place_by_id(p[1])[6]
        pic_url = 'images/'+ pic
        date_review = p[3]
        rating = p[6]
        review = p[4]
        js_rev = {"date_review":date_review, "rating":rating, "review":review, "pic_loc":pic_url}
        my_rev.append(js_rev)
    for p in data2:
        pic_url = 'images/' + p[1]
        rev = dbUtils.get_place_review(p[0])
        for i in rev:
            us_id = i[2]
            user_nam = dbUtils.get_username(us_id)[0]
            date_review = i[3]
            rating = i[6]
            review = i[4]
            js_rev = {"date_review":date_review, "rating":rating, "review":review, "user_name":user_nam,"pic_loc":pic_url}
            review_dic.append(js_rev)

    return render_template('user_reviews.html', my_rev = my_rev, to_me_rev = review_dic, username=username1)

@review_bp.route('/dashboard_user/post_review',methods=['POST'])
@login_required
def add_review():
    user_id = current_user.user_id
    place_id = request.args.get('place_id')
    rating = request.form['optradio']
    review = request.form['review_post']
    dbUtils.post_review(place_id,user_id,review,rating)
    return redirect(url_for('listing_bp.show_selected_place', place_id=place_id))
