import os
import psycopg2 as dbapi2
from flask import Flask, Response, render_template, jsonify, request, make_response
import urllib.parse, json
from os.path import exists
from os import makedirs
from flask_cors import CORS, cross_origin
from database import *

# url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
# db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)

db = DatabaseManager()

app = Flask(__name__, template_folder="../")
cors = CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


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


@app.route('/add_user', methods=["POST"])
def add_user():
    """
    Adds a new student to the database, used for sign up
    Input {"name": name, "email": email, "password": password , "isstudent": true/false}
    Output {"status": true/false, "usid": userid, "isstudent": true/false}        status is true if the user could be signed up
    """
    data = json.loads(json.dumps(request.get_json()))
    name = data["name"]
    email = data["email"]
    password = data["password"]
    isstudent = bool(data["isstudent"])
    usid = int(db.generate_new_usid())

    print(isstudent)
    print('student am I?')
    # add hash password function around here
    status = db.add_user(usid, name, email, password, isstudent)
    return jsonify({"status": status, "usid": usid, "isstudent": isstudent})


@app.route('/add_student', methods=["POST"])
def add_student():
    """
    Adds a student to a class in the database TODO: (Check if the current user is allowed to do so)
    Input {"email": email, "classid": classid}
    Output {"status": true/false}       status is true if adding the student was successful
    """
    data = json.loads(json.dumps(request.get_json()))
    email = data["email"]
    classid = int(data["classid"])
    status = db.add_student(email, classid)
    return jsonify({"status": status})


@app.route('/save_class', methods=["POST"])
def save_class():
    """
    Create a new class in the database TODO: (Check if the current user is allowed to do so)
    Input {"classname": name of class, "instructorid": instructorid}
    Output {"status": true/false, "classid": classid of created class} status is true if the class was created, classid is None/null if status is false
    """
    data = json.loads(json.dumps(request.get_json()))
    classname = data["classname"]
    instructorid = int(data["instructorid"])
    classid = int(db.generate_new_classid())
    status = db.save_class(classid, classname, instructorid)
    return jsonify({"status": status, "classid": classid})


@app.route('/verify_user_login', methods=["POST"])
def verify_user_login():
    """
    returns true if the username and passwordhash match the database false otherwise
    Input {"email": email, "password": password}
    Output {"status": true/false, "usid": userid of logged in user, "isstudent": true/false}
    status is true if login was sucessful usid is None/null if login was unsucessful
    """
    data = json.loads(json.dumps(request.get_json()))
    email = data["email"]
    password = data["password"]
    status, usid, isstudent = db.verify_user_login(email, password)
    return jsonify({"status": status, "usid": usid, "isstudent": isstudent})


@app.route('/add_lecture', methods=["POST"])
def add_lecture():
    """
    adds a lecture to the specified class
    Input {"instructorid": instructorid of instructor making class, "classid": classid where lecture is to be created, "starttime": starttme of lecture
    ,"endtime": endtime of lecture, "lectureurl": url of lecture, "day": day of lecture }

    Output {"status": true/false, "lectureid": id of added lecture} status is true if lecture could be added
    Example Input: {"instructorid": 4, "classid" : 1, "starttime" :'03:00:00', "endtime" : '05:00:00', "lectureurl" :'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    , "day" :'2001-10-05'}
    """
    data = json.loads(json.dumps(request.get_json()))
    instructorid = int(data["instructorid"])
    classid = int(data["classid"])
    starttime = data["starttime"]
    endtime = data["endtime"]
    lectureurl = data["lectureurl"]
    day = data["day"]
    lectureid = int(db.generate_new_lectureid(classid))
    status = db.add_lecture(instructorid, lectureid, classid, starttime, endtime, lectureurl, day)
    return jsonify({"status": status, "lectureid": lectureid})


@app.route('/get_all_lectures', methods=['POST'])
def get_all_lectures():
    """
    returns all the lectures of a given class that a user is in
    Input {"usid": userid of student/professor in a class, "classid": classid}
    Output {"result": list of jsons}
    element in list of jsons = {
            "day": day,
            "endtime": time,
            "lectureid": lectureid,
            "starttime": starttime
        }
    """
    data = json.loads(json.dumps(request.get_json()))
    usid = int(data["usid"])
    classid = int(data["classid"])
    result = db.get_all_lectures(usid, classid)
    data = []
    for lecture in result:
        print(type(lecture[2]))
        json_data = {"lectureid": lecture[0], "starttime": str(lecture[2]), "endtime": str(lecture[3]),
                     "day": str(lecture[5])}
        data.append(json_data)
    return jsonify({"result": data})


@app.route('/get_all_classes', methods=['POST'])
def get_all_classes():
    """
    returns all the classes of a student
    Input {"studentid": id of student}
    Output {"result": list of jsons}
    element in list of jsons = {
            "classid": 1,
            "classname": "SD and D",
            "instructor": "Goldschmidt"
        }
    """
    data = json.loads(json.dumps(request.get_json()))
    studentid = int(data["studentid"])
    result = db.get_all_classes(studentid)
    data = []
    for c in result:
        json_data = {"classid": c[0], "classname": c[1], "instructor": c[2]}
        data.append(json_data)
    return jsonify({"result": data})


@app.route('/get_all_teaching', methods=['POST'])
def get_all_teaching():
    """
    returns all the courses an instructor teaches
    Input {"instructorid": id of instructor}
    Output {"result": list of jsons}
    element in list of jsons =         {
            "classid": 1,
            "classname": "SD and D"
        }
    """
    data = json.loads(json.dumps(request.get_json()))
    instructorid = int(data["instructorid"])
    result = db.get_all_teaching(instructorid)
    data = []
    for c in result:
        json_data = {"classid": c[0], "classname": c[1]}
        data.append(json_data)
    return jsonify({"result": data})


@app.route('/get_lecture_url', methods=['POST'])
def get_lecture_url():
    """
    returns the url of the lecture coresponding to the lectureid and classid
    Input: {"classid": classid, "lectureid": lectureid}
    Output: {"url": url} url will be False if no url matching these parameters could be found
    """
    data = json.loads(json.dumps(request.get_json()))
    lectureid = int(data['lectureid'])
    classid = int(data['classid'])
    url = db.get_lecture_url(lectureid, classid)
    return jsonify({"url": url})


@app.route('/reset_database', methods=['GET'])
def reset_database():
    """
    resets all the tables in the database (DEV/ADMIN FUNCTION)
    """
    db.reset_database()
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
