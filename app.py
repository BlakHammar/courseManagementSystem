from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/addCourse')
def new_course():
    return render_template('addCourse.html')

@app.route('/getCourses')
def getCourses():
    return render_template('getCourses.html')

@app.route('/listByInstructor')
def listByInstructor():
    return render_template('listByInstructor.html')

@app.route('/getDepts')
def getDepts():
    return render_template('getDept.html')

@app.route('/top5dept')
def top5dept():
    return render_template('top5dept.html')



@app.route('/addrec', methods=['POST', 'GET'])
def add_course():
    if request.method == 'POST':
        try:
            courseID = request.form['courseID']
            department = request.form['department']
            semester = request.form['semester']
            enrollment = request.form['enrollment']
            instructorID = request.form['instructorID']

            name = request.form['name']
            department2 = request.form['department2']
            jobTitle = request.form['jobTitle']
            salary = 65000.00


            with sql.connect("courseData.db") as con:
                cur = con.cursor()

                cur.execute('''INSERT INTO Courses (CourseID, Department, Semester, Enrollment, InstructorID)
                   VALUES (?, ?, ?, ?, ?, ?)''', (courseID, department, semester, enrollment, instructorID))

                cur.execute('''INSERT INTO Employees (EmployeeID, Name, Department, JobTitle, Salary)
                   VALUES (?, ?, ?, ?, ?)''', (instructorID, name, department2, jobTitle, salary))

                con.commit()
                msg = "Record successfully added"

        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template('index.html',)
            con.close()


@app.route('/getrec', methods=['POST'])
def getrec():
    instructorID = request.form['instructorID']

    con = sql.connect('courseData.db')
    cur = con.cursor()
    courses = cur.execute('SELECT * FROM Courses WHERE InstructorID = ?', (instructorID,)).fetchall()
    con.close()

    return render_template('listByInstructor.html', courses=courses)



@app.route('/getDept', methods=['POST'])
def getDept():
    department = request.form['department']

    con = sql.connect('courseData.db')
    cur = con.cursor()
    courses = cur.execute('SELECT * FROM Courses WHERE Department = ? ORDER BY Enrollment DESC LIMIT 5', (department,)).fetchall()
    con.close()

    return render_template('top5dept.html', courses=courses)



if __name__ == '__main__':
    app.run(debug=True)
