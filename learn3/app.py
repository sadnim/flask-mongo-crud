from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId  

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.learn

@app.route('/')
def index():
    return redirect(url_for('courses'))

#courses routes

@app.route('/courses')
def courses():
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'title')  # Default sort by title
    sort_order = request.args.get('sort_order', 'asc')  # Default sort order ascending

    if search:
        courses = db.courses.find({'title': {'$regex': search, '$options': 'i'}})
    else:
        courses = db.courses.find().sort([(sort_by, 1 if sort_order == 'asc' else -1)])

    return render_template('courses.html', courses=courses)


@app.route('/add_course', methods=['POST'])
def add_course():
    title = request.form.get('title')
    teacher = request.form.get('teacher')
    new_course = {'title': title, 'teacher': teacher, 'students': []}
    db.courses.insert_one(new_course)
    return redirect(url_for('courses'))

@app.route('/edit_course/<string:id>', methods=['GET', 'POST'])
def edit_course(id):
    if request.method == 'POST':
        title = request.form.get('title')
        teacher = request.form.get('teacher')
        db.courses.update_one({'_id': ObjectId(id)}, {'$set': {'title': title, 'teacher': teacher}})
        return redirect(url_for('courses'))
    else:
        course = db.courses.find_one({'_id': ObjectId(id)})
        return render_template('edit_course.html', course=course)

@app.route('/delete_course/<string:id>', methods=['POST'])
def delete_course(id):
    db.courses.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('courses'))


#students routes


@app.route('/students')
def students():
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'name')  # Default sort by name
    sort_order = request.args.get('sort_order', 'asc')  # Default sort order ascending

    if search:
        students = db.students.find({'name': {'$regex': search, '$options': 'i'}})
    else:
        students = db.students.find().sort([(sort_by, 1 if sort_order == 'asc' else -1)])

    return render_template('students.html', students=students)


@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    courses = request.form.getlist('courses')
    new_student = {'name': name, 'courses': courses}
    db.students.insert_one(new_student)
    return redirect(url_for('students'))

@app.route('/edit_student/<string:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        name = request.form.get('name')
        courses = request.form.getlist('courses')
        db.students.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'courses': courses}})
        return redirect(url_for('students'))
    else:
        student = db.students.find_one({'_id': ObjectId(id)})
        courses = db.courses.find()
        return render_template('edit_student.html', student=student, courses=courses)

@app.route('/delete_student/<string:id>', methods=['POST'])
def delete_student(id):
    db.students.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('students'))

#teachers routes



@app.route('/teachers')
def teachers():
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'name')  # Default sort by name
    sort_order = request.args.get('sort_order', 'asc')  # Default sort order ascending

    if search:
        teachers = db.teachers.find({'name': {'$regex': search, '$options': 'i'}})
    else:
        teachers = db.teachers.find().sort([(sort_by, 1 if sort_order == 'asc' else -1)])

    return render_template('teachers.html', teachers=teachers)

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    name = request.form.get('name')
    courses = request.form.getlist('courses')
    new_teacher = {'name': name, 'courses': courses}
    db.teachers.insert_one(new_teacher)
    return redirect(url_for('teachers'))

@app.route('/edit_teacher/<string:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    if request.method == 'POST':
        name = request.form.get('name')
        courses = request.form.getlist('courses')
        db.teachers.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'courses': courses}})
        return redirect(url_for('teachers'))
    else:
        teacher = db.teachers.find_one({'_id': ObjectId(id)})
        courses = db.courses.find()
        return render_template('edit_teacher.html', teacher=teacher, courses=courses)

@app.route('/delete_teacher/<string:id>', methods=['POST'])
def delete_teacher(id):
    db.teachers.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('teachers'))

if __name__ == '__main__':
    app.run(debug=True)
