from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

# Code goes here

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    student_github_tuple = hackbright_app.get_student_by_github(student_github)
    first_name = student_github_tuple[0]
    last_name = student_github_tuple[1]
    github = student_github_tuple[2]
    
    student_grades_list = hackbright_app.get_grades_by_student(first_name,last_name)
    # title = student_grades_tuple[0]
    # grade = student_grades_tuple[1]
    # max_grade = student_grades_tuple[2]

    html = render_template("student_info.html", first_name=first_name,
                                                last_name=last_name,
                                                github=github,
                                                student_grades_list=student_grades_list)
    return html

if __name__ == "__main__":
    app.run(debug=True)