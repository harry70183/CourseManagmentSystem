from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table(
    "asscociation",
    db.Model.metadata,
    db.Column("assignment_id", db.Integer, db.ForeignKey("assignment.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

# your classes here
class Course(db.Model):
    """
    Course Model
    Create 6 columns: id, code, name, assignments, instructors, students

    col_name     dtype      description
    id           INT        course_id
    code         STRING     course code (e.g. CS 1998)
    name         STRING     course name (e.g. Intro to Backend Development)
    assignments  COLLECTION assignments of this course
    instructors  COLLECTION instructors teaching this course
    students     COLLECTION students taking this course
    """
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    code = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)

    assignments = db.relationship("Assignment", secondary=association_table, back_populates="users")
    instructors = db.relationship("User", secondary=association_table, back_populates="users")
    students = db.relationship("User", secondary=association_table, back_populates="users")

    def __init__(self, **kwargs):
        """
        Initialize a Course Object
        """
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serialize a Course object
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.simple_serialize() for a in self.assignments],
            "instructors": [i.simple_serialize() for i in self.instructors],
            "students":[s.simple_serialize() for s in self.students] 
        }
    def simple_serialize(self):
        """
        Serialize a course object without assignment, student, and instructor fields 
        """
        return {"id": self.id, "code": self.code, "name": self.name}

class User(db.Model):
    """
    User Model
    Create 3 columns: id, code, name, courses

    col_name    dtype       description
    id          INT         user id
    name        STRING      user name (e.g. Raahi Menon)
    netid       STRING      net id/school account (e.g. rm834)
    courses     COLLECTION  courses taken by this student
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)

    courses = db.relationship("Course", secondary=association_table, back_populates=True)

    def __init__(self, **kwargs):
        """
        Initialize a User Object
        """
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")

    def serialize(self):
        """
        Serialize a User object
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [c.simple_serialize() for c in self.courses]
        }
    def simple_serialize(self):
        """
        Serialize a User object without course field
        """      
        return {"id": self.id,"name": self.name,"netid": self.netid}

class Assignment(db.Model):
    """
    Assignment Model
    """
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course = db.relationship("Course", secondary=association_table, back_populates=True)

    def __init__(self, **kwargs):
        """
        Initialize a assignment object
        """
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", -1)
        self.course_id = kwargs.get("course_id")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": self.course.simple_serialize()
        }    