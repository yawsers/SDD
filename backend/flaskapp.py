import os
import psycopg2 as dbapi2
from flask import Flask, jsonify, request, make_response
import urllib.parse, json
from os.path import exists
from os import makedirs
from flask_cors import CORS, cross_origin
from database import *

#url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
#db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)

db = DatabaseManager()


app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def hello():
    return 'Hello World!'
'''
@app.route('/users')
def users():
    #returns all users
    users = []
    try:
        cur.execute ("SELECT * FROM users")
        rows = cur.fetchall()
        for i, row in enumerate(rows):
            users.append(row[1])
        return jsonify({"users": users})
    except Exception as e:
        print(e)
        return []
'''



@app.route('/add_user', methods = ["POST"])
def add_user():
    '''
    Adds a new student to the database
    '''
    data = json.loads(json.dumps(request.get_json()))
    name = data["name"]
    email = data["email"]
    password = data["password"]
    isstudent = bool(data["isstudent"])
    usid = db.generate_new_usid()

    #add hash password function around here
    status = db.add_user(usid, name, email, password, isstudent)
    return jsonify({"status":status})

@app.route('/add_student', methods = ["POST"])
def add_student():
    '''
    Adds a student to a class in the database TODO: (Check if the current user is allowed to do so)
    '''
    data = json.loads(json.dumps(request.get_json()))
    usid = data["usid"]
    classid = data["classid"]
    status = db.add_student(usid,classid)
    return jsonify({"status":status})
    

@app.route('/save_class', methods = ["POST"])
def save_class():
    '''
    Create a new class in the database TODO: (Check if the current user is allowed to do so)
    '''
    data = json.loads(json.dumps(request.get_json()))
    classname = data["classname"]
    instructorid = int(data["instructorid"])
    classid = db.generate_new_classid()
    status = db.save_class(classid, classname, instructorid)
    return jsonify({"status":status})

@app.route('/verify_user_login', methods = ["POST"])
def verify_user_login():
    '''
    returns true if the username and passwordhash match the database false otherwise
    '''
    data = json.loads(json.dumps(request.get_json()))
    email = data["email"]
    password = data["password"]
    status = db.verify_user_login(email, password)
    return jsonify({"status":status})

@app.route('/add_lecture', methods = ["POST"])    
def add_lecture():
    data = json.loads(json.dumps(request.get_json()))
    instructorid = data["lectureid"]
    classid = data["classid"]
    starttime = data["starttime"]
    endtime = data["endtime"]
    lectureurl = data["lectureurl"]
    day = data["day"]
    lectureid = db.generate_new_lectureid(classid)
    status = db.add_lecture(instructorid, lectureid, classid, starttime, endtime, lectureurl, day)
    return jsonify({"status":status})

@app.route('/get_all_lectures', methods = ['POST'])
def get_all_lectures(self,usid, classid):
    '''
    returns all the lectures of a given class that a user is in
    '''
    data = json.loads(json.dumps(request.get_json()))
    usid = data["usid"]
    classid = data["classid"]
    result = db.get_all_lectures(usid, classid)
    return json({"result": result})

@app.route('/get_all_classes', methods = ['POST'])
def get_all_classes(self, studentid):
    '''
    returns all the classes of a student
    '''
    data = json.loads(json.dumps(request.get_json()))
    studentid = data["studentid"]
    result = db.get_all_classes(studentid)
    return jsonify({"result": result})


@app.route('/reset_database', methods = ['GET'])
def reset_database(self):
    '''
    resets all the tables in the database (DEV/ADMIN FUNCTION)
    '''
    db.resest_database()
    return 'DONE', 201


'''
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
'''


if __name__ == '__main__':
    app.run(debug=True)