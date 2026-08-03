from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Response,
    flash
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from sqlalchemy import or_
from sqlalchemy import or_, asc, desc, func
import csv
import io

app = Flask(__name__)

from models.student import db, Student, Admin
# ===========================
# Flask Configuration
# ===========================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "student-management-secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please login first."
login_manager.login_message_category = "warning"

# Initialize Database
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Create Database Tables
with app.app_context():
    db.create_all()


# ===========================
# Dashboard
# ===========================
from sqlalchemy import func

@app.route("/")
def dashboard():

    students = Student.query.all()

    total_students = len(students)

    average_marks = round(
        db.session.query(func.avg(Student.marks)).scalar() or 0,
        2
    )

    highest_marks = db.session.query(func.max(Student.marks)).scalar() or 0

    total_courses = db.session.query(Student.course).distinct().count()

    top_students = (
        Student.query
        .order_by(Student.marks.desc())
        .limit(5)
        .all()
    )

    recent_students = (
        Student.query
        .order_by(Student.id.desc())
        .limit(5)
        .all()
    )

    course_data = (
        db.session.query(
            Student.course,
            func.count(Student.id)
        )
        .group_by(Student.course)
        .all()
    )

    course_labels = [c[0] for c in course_data]
    course_counts = [c[1] for c in course_data]

    return render_template(
        "dashboard.html",
        total_students=total_students,
        average_marks=average_marks,
        highest_marks=highest_marks,
        total_courses=total_courses,
        top_students=top_students,
        recent_students=recent_students,
        course_labels=course_labels,
        course_counts=course_counts
    )
# ===========================
# View Students
# ===========================
@app.route("/students")
@login_required
def students():

    page = request.args.get("page", 1, type=int)

    per_page = 5

    keyword = request.args.get("keyword", "")

    course = request.args.get("course", "")

    sort = request.args.get("sort", "")

    order = request.args.get("order", "asc")

    query = Student.query

    # Search
    if keyword:
        query = query.filter(Student.name.ilike(f"%{keyword}%"))

    # Filter
    if course:
        query = query.filter(Student.course == course)

    # Sorting
    if sort:

        column = getattr(Student, sort)

        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    students = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    courses = (
        db.session.query(Student.course)
        .distinct()
        .all()
    )

    return render_template(
        "students.html",
        students=students,
        courses=courses,
        keyword=keyword,
        course=course,
        sort=sort,
        order=order
    )

# ===========================
# Add Student
# ===========================
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_student():

    if request.method == "POST":

        student = Student(
            name=request.form["name"],
            age=int(request.form["age"]),
            course=request.form["course"],
            marks=float(request.form["marks"])
        )

        db.session.add(student)
        db.session.commit()

        flash("Student added successfully!", "success")

        return redirect(url_for("students"))

    return render_template("add_student.html")


# ===========================
# Edit Student
# ===========================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.name = request.form["name"]
        student.age = int(request.form["age"])
        student.course = request.form["course"]
        student.marks = float(request.form["marks"])

        db.session.commit()

        flash("Student updated successfully!", "success")

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student
    )


# ===========================
# Delete Student
# ===========================
@app.route("/delete/<int:id>")
@login_required
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "danger")

    return redirect(url_for("students"))


# ===========================
# Search Student
# ===========================
@app.route("/search", methods=["GET"])
@login_required
def search():

    keyword = request.args.get("keyword", "")

    students = Student.query.filter(
        or_(
            Student.name.ilike(f"%{keyword}%"),
            Student.course.ilike(f"%{keyword}%")
        )
    ).all()

    return render_template(
        "search.html",
        students=students,
        keyword=keyword
    )

    keyword = request.args.get("keyword", "")

    students = Student.query.filter(
        or_(
            Student.name.ilike(f"%{keyword}%"),
            Student.course.ilike(f"%{keyword}%")
        )
    ).all()

    return render_template(
        "search.html",
        students=students,
        keyword=keyword
    )


# ===========================
#  Export Student
# ===========================

@app.route('/export-students')
@login_required
def export_students():

    students = Student.query.all()

    output = io.StringIO()

    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "ID",
        "Name",
        "Age",
        "Course",
        "Marks"
    ])

    # CSV Data
    for student in students:
        writer.writerow([
            student.id,
            student.name,
            student.age,
            student.course,
            student.marks
        ])


    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=students.csv"
    )

    return response


# ===========================
# Login Rout
# ===========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username
        ).first()

        if admin and admin.check_password(password):

            login_user(admin)

            flash(
                "Login successful!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password",
            "danger"
        )

    return render_template("login.html")

# ===========================
# Logout Route
# ===========================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))
# ===========================
# Run Application
# ===========================
if __name__ == "__main__":
    app.run(debug=True)