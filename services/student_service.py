from models.student import Student
from utils.file_handler import load_students, save_students


class StudentService:

    def add_student(self):
        students = load_students()

        student_id = input("Enter Student ID: ")

        # Check if ID already exists
        for student in students:
            if student["student_id"] == student_id:
                print("Student ID already exists!")
                return

        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        course = input("Enter Course: ")
        marks = float(input("Enter Marks: "))

        student = Student(student_id, name, age, course, marks)

        students.append(student.to_dict())

        save_students(students)

        print("Student added successfully!")

    def view_students(self):
        students = load_students()

        if not students:
            print("\nNo students found.")
            return

        print("\n----- Student Records -----")

        for student in students:
            print(f"""
ID     : {student['student_id']}
Name   : {student['name']}
Age    : {student['age']}
Course : {student['course']}
Marks  : {student['marks']}
-----------------------------
""")

    def search_student(self):
        students = load_students()

        student_id = input("Enter Student ID to search: ")

        for student in students:
            if student["student_id"] == student_id:
                print("\nStudent Found")
                print(student)
                return

        print("Student not found.")

    def update_student(self):
        students = load_students()

        student_id = input("Enter Student ID to update: ")

        for student in students:

            if student["student_id"] == student_id:

                student["name"] = input("Enter New Name: ")
                student["age"] = int(input("Enter New Age: "))
                student["course"] = input("Enter New Course: ")
                student["marks"] = float(input("Enter New Marks: "))

                save_students(students)

                print("Student updated successfully!")

                return

        print("Student not found.")

    def delete_student(self):
        students = load_students()

        student_id = input("Enter Student ID to delete: ")

        for student in students:

            if student["student_id"] == student_id:

                students.remove(student)

                save_students(students)

                print("Student deleted successfully!")

                return

        print("Student not found.")