# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


# class Student(db.Model):
#     __tablename__ = "students"

#     id = db.Column(db.Integer, primary_key=True)

#     name = db.Column(db.String(100), nullable=False)

#     age = db.Column(db.Integer, nullable=False)

#     course = db.Column(db.String(100), nullable=False)

#     marks = db.Column(db.Float, nullable=False)

#     def __repr__(self):
#         return f"<Student {self.name}>"


from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    age = db.Column(db.Integer, nullable=False)

    course = db.Column(db.String(100), nullable=False)

    marks = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Admin {self.username}>"
