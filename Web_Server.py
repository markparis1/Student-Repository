from flask import Flask, render_template
from typing import Dict
import sqlite3


app: Flask = Flask(__name__)

@app.route('/Web_Server')
def web_server() -> str:
    return "Hello World!"

@app.route('/students')
def students_summary() -> str:
    query = "SELECT Students.Name as Student, Students.CWID, Course, Grade, Instructors.Name as Instructor From Grades Join Students on Grades.StudentCWID = Students.CWID Join Instructors on Grades.InstructorCWID = Instructors.CWID Order BY Students.Name"

    db: sqlite3.Connection = sqlite3.connect("/Users/MyICloud/Developer/810_startup.db")

    data: Dict[str,str] = \
        [{'name': name, 'cwid': cwid, 'course': course, 'grade':grade, 'instructor': instructor}
            for name, cwid, course, grade, instructor in db.execute(query)]
    
    db.close()

    return render_template('student_table.html',
                            title = "Stevens Repository",
                            table_title = "Student, Course, Grade, and Instructor",
                            students=data)



app.run(debug=True)