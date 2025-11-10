import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from db.dbhelper import *
import sys
sys.path.insert(0, "db/")


app = Flask(__name__)


@app.route("/")
def index() -> None:
    students = getAll('students')
    return render_template('index.html', studentlist=students)


@app.route('/add', methods=['POST'])
def add_student():
    idno = request.form['idno']
    lastname = request.form['lastname']
    firstname = request.form['firstname']
    course = request.form['course']
    level = request.form['level']

    addRecord("students", idno=idno, lastname=lastname,
              firstname=firstname, course=course, level=level)
    return redirect(url_for('index'))


@app.route('/delete/<idno>')
def delete_student(idno):
    deleteRecord("students", idno=idno)
    return redirect(url_for('index'))


@app.route("/update/<idno>", methods=['GET', 'POST'])
def update_student(idno):
    if request.method == 'POST':
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        course = request.form['course']
        level = request.form['level']

        updateRecord("students",
                     idno=idno,
                     lastname=lastname,
                     firstname=firstname,
                     course=course,
                     level=level)
        return redirect(url_for('index'))

    student = getRecord("students", idno=idno)
    students = getAll('students')

    return render_template('index.html', student=student[0], studentlist=students)


if __name__ == "__main__":
    app.run(debug=True)
