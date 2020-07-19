from connection import conn

#for user
def signup(username, email, password):
    conn.connect()
    cur = conn.cursor()
    sql_string = "INSERT INTO users (userName, email, password) VALUES(%s, %s, %s)"
    cur.execute(sql_string, (username, email, password))
    conn.commit()
    cur.close()
    conn.close()

def login(username):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM users WHERE userName= %s"
    cur.execute(sql_string,(username, ))
    info = cur.fetchone()
    conn.close()
    return info

def get_user(user_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM users WHERE userID= %s"
    cur.execute(sql_string,(user_id, ))
    info = cur.fetchone()
    conn.close()
    return info[1]

def get_username(user_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT userName FROM users WHERE userID= %s"
    cur.execute(sql_string,(user_id, ))
    info = cur.fetchone()
    conn.close()
    return info

def get_by_username(username):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM users WHERE userName= %s"
    cur.execute(sql_string,(username, ))
    info = cur.fetchone()
    conn.close()
    return info

def get_email(email):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM users WHERE email= %s"
    cur.execute(sql_string,(email, ))
    info = cur.fetchone()
    conn.close()
    return info


class user():
    def __init__(self, user_id):
        self.user_id = user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

    def get_username(self):
        try:
            return get_user(self.user_id)[1]
        except:
            return "Visitor"


#for places
def new_place(user_id, name, address, website, phone, image_loc, description):
    conn.connect()
    cur = conn.cursor()
    sql_string = "INSERT INTO places (userID, name, address, website, phone, image_location, description, postedDate) VALUES (%s, %s, %s, %s, %s, %s, %s, now())"
    cur.execute(sql_string,(user_id, name, address, website, phone, image_loc, description))
    conn.commit()
    cur.close()
    conn.close()

def delete_place(place_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "DELETE FROM places WHERE placeID = %s"
    cur.execute(sql_string,(place_id, ))
    conn.commit()
    cur.close()
    conn.close()

def delete_review(place_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "DELETE FROM review WHERE placeID = %s"
    cur.execute(sql_string,(place_id, ))
    conn.commit()
    cur.close()
    conn.close()

def get_place_by_user(user_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM places WHERE userID = %s ORDER BY postedDate DESC"
    cur.execute(sql_string,(user_id, ))
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info



def get_place_by_name(name):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM places WHERE name = %s"
    cur.execute(sql_string,(name, ))
    info = cur.fetchone()
    cur.close()
    conn.close()
    return info

def get_place_by_name1(name):
    name = '%'+name+'%'
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM places WHERE name LIKE %s"
    cur.execute(sql_string,(name, ))
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info

def get_place_by_id(place_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM places WHERE placeID = %s"
    cur.execute(sql_string,(place_id, ))
    info = cur.fetchone()
    cur.close()
    conn.close()
    return info

def get_all_places():
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM places WHERE approved = 0 ORDER BY postedDate DESC"
    cur.execute(sql_string)
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info

#for admin
def approve_place(place_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "UPDATE places SET approved = 1 WHERE placeID = %s "
    cur.execute(sql_string,(place_id, ))
    conn.commit()
    cur.close()
    conn.close()

def block_user(user_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "UPDATE users SET isBlock = 1 WHERE userID = %s "
    cur.execute(sql_string,(user_id, ))
    conn.commit()
    cur.close()
    conn.close()

def get_to_approve():
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM places WHERE approved = false ORDER BY postedDate DESC"
    cur.execute(sql_string,)
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info

#for review
def post_review(place_id, user_id,review,rating):
    conn.connect()
    cur = conn.cursor()
    sql_string = "INSERT INTO review (placeID, userID, reviewDate, review,rating) VALUES(%s, %s,now(), %s, %s)"
    cur.execute(sql_string,(place_id,user_id,review,rating))
    conn.commit()
    cur.close()
    conn.close()


def get_review_by_user(user_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM review WHERE userID =%s ORDER BY reviewDate DESC"
    cur.execute(sql_string,(user_id,))
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info

def get_all_place_user(user_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT placeID,image_location FROM places WHERE userID =%s ORDER BY postedDate DESC"
    cur.execute(sql_string,(user_id,))
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info

def get_all_place_review(place_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM review WHERE placeID =%s ORDER BY reviewDate DESC"
    cur.execute(sql_string,(place_id,))
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info

def get_place_review(place_id):
    conn.connect()
    cur = conn.cursor()
    sql_string = "SELECT * FROM review WHERE placeID =%s ORDER BY reviewDate DESC"
    cur.execute(sql_string,(place_id,))
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info
