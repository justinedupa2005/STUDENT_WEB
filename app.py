import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from db.dbhelper import *
import sys
sys.path.insert(0, "db/")

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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

    # Handle image upload
    image_file = request.files.get('image')
    image_filename = None
    if image_file and image_file.filename != '':
        image_filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image_file.save(image_path)

    # Add student record including image
    addRecord("students", idno=idno, lastname=lastname,
              firstname=firstname, course=course, level=level,
              image=image_filename)

    return redirect(url_for('index'))


@app.route('/delete/<idno>')
def delete_student(idno):
    deleteRecord("students", idno=idno)
    return redirect(url_for('index'))


@app.route("/update/<idno>", methods=['GET', 'POST'])
def update_student(idno):
    student = getRecord("students", idno=idno)
    if not student:
        return redirect(url_for('index'))
    student = student[0]  # Extract dict from list

    if request.method == 'POST':
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        course = request.form['course']
        level = request.form['level']

        # Handle image upload
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
        else:
            # Keep the previous image if it exists
            image_filename = student['image']

        # Update student record
        updateRecord("students",
                     idno=idno,
                     lastname=lastname,
                     firstname=firstname,
                     course=course,
                     level=level,
                     image=image_filename)
        return redirect(url_for('index'))

    students = getAll('students')
    return render_template('index.html', student=student, studentlist=students)


if __name__ == "__main__":
    app.run(debug=True)
