import sqlite3
from flask import Flask, render_template

conn = sqlite3.connect('courseData.db')

conn.execute('''CREATE TABLE Employees 
(EmployeeID TEXT PRIMARY KEY, 
Name TEXT, 
Department TEXT, 
JobTitle TEXT,
Salary FLOAT)''')

conn.execute(''' CREATE TABLE Courses 
( CourseID TEXT, 
Department TEXT, 
Semester TEXT, 
InstructorID TEXT,
Enrollment INTEGER, FOREIGN KEY 
(InstructorID) REFERENCES Employees (EmployeeID)
)
''')


conn.close()
