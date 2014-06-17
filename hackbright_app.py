import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def make_new_student(first_name,last_name,github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name,last_name,github))
    CONN.commit()
    print "Successfully added student: %s %s, %s" % (first_name, last_name, github)

def get_grade_by_project(first_name,last_name,project_title):
    query = """SELECT Students.first_name,Students.last_name,Grades.project_title,Grades.grade FROM Grades JOIN Students ON (Students.github = Grades.student_github) WHERE first_name = ? AND last_name = ? AND project_title = ?"""
    DB.execute(query, (first_name,last_name,project_title,))
    row = DB.fetchone()
    print """\
Student: %s %s
Project: %s
Grade: %d""" % (row[0],row[1],row[2],row[3])

def get_project_by_title(title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query,(title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s"""%(row[0],row[1])

def make_new_project(title,description,max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s, max pts: %s" % (title, description, max_grade)

def make_new_grade(student_github,title,grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (student_github, title, grade))
    CONN.commit()
    print "Successfully added grade: %s, %s, points: %s" % (student_github, title, grade)

def get_grades_by_student(first_name,last_name):
    query = """SELECT Projects.title, Grades.grade, Projects.max_grade FROM Projects JOIN Grades ON (Projects.title = Grades.project_title) JOIN Students ON (Students.github = Grades.student_github) WHERE first_name = ? AND last_name = ?"""
    DB.execute(query, (first_name,last_name,))
    rows = DB.fetchall()
    for row in rows:
        print """\
Project title: %s 
Grade: %s 
Max points: %s""" % (row[0],row[1],row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "description":
            get_project_by_title(*args)
        elif command == "new_project":
            args = " ".join(tokens[1:]).split(', ')
            make_new_project(*args)
        elif command == "student_project_grade":
            args = " ".join(tokens[1:]).split(', ')
            get_grade_by_project(*args)
        elif command == "new_grade":
            args = " ".join(tokens[1:]).split(', ')
            make_new_grade(*args)
        elif command == "student_grades":
            get_grades_by_student(*args)



    CONN.close()

if __name__ == "__main__":
    main()
