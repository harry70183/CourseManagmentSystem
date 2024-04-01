from db import db, Course, User, Assignment
from flask import Flask, request
import json
import os

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# -- COURSE ROUTES ------------------------------------------------------

@app.route('/')
def greeting():
    return f"Hello {os.environ['NAME']}! Your NETID is {os.environ['NETID']}"

@app.route("/api/courses/")
def get_courses():
    """
    Web Service Endpoint for getting all courses
    """
    courses = [course.serialize() for course in Course.query.all()]
    return success_response({"courses": courses})

@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Endpoint for creating a new course
    """
    body = json.loads(request.data)
    if body.get("code")==None or body.get("name")==None:
        return failure_response("Course code or name not provided", 400)
    
    new_course = Course(code = body.get("code"), name = body.get("name"))
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)

@app.route("/api/courses/<int:course_id>/")
def get_course(course_id):
    """
    Endpoint for getting a course by id
    """
    course = Course.query.filter_by(id = course_id).first()
    if course is None:
        return failure_response(f"Course {course_id} is not found")
    return success_response(course.serialize())

@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    Endpoint for deleting a course by id
    """
    course = Course.query.filter_by(id = course_id).first()
    if course is None:
        return failure_response(f"Task {course_id} is not found")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize()) 

# -- USER ROUTES ------------------------------------------------------
@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)

    if body.get("name")==None or body.get("netid")==None:
        return failure_response("User name or netid not provided", 400)
    
    new_user = User(name = body.get("name"), netid = body.get("netid"))
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return failure_response(f"User {user_id} is not found")
    return success_response(user.serialize())

@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def assign_user(course_id):
    """
    Endpoint for assigning a user
    to a course by course id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response(f"Course {course_id} is not found")
    body = json.loads(request.data)
    user_id = body.get("user_id")
    type = body.get("type")

    user = User.query.filter_by(color = user).first()
    if user == None:
        return failure_response(f"user {user_id} is not found")
    if type == "instructor":
        course.instructors.append(user)
    elif type == "student":
        course.students.append(user)
    else:
        return failure_response("Please choose student or instructor in type")        
    db.session.commit()
    return success_response(course.serialize())

# -- ASSIGNMENT ROUTES ------------------------------------------------------
@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    """
    Endpoint for creating an assignment
    for a course by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response(f"Course {course_id} is not found")
    
    body = json.loads(request.data)
    if body.get("title") == None or body.get("due_date")==None:
        return failure_response("Assignment title or due date not provided", 400)
    
    newAssignment= Assignment(
        title = body.get("title"),
        due_date = body.get("due_date"),
        course_id = course_id
    )
    db.session.add(newAssignment)
    db.session.commit()
    return success_response(newAssignment.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
