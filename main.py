from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'university_secret_key'

# In-memory user storage with roles
users = {
    'admin': {'password': 'admin123', 'role': 'staff'},
    'student1': {'password': 'password123', 'role': 'student'}
}


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            if session['role'] == 'staff':
                return redirect(url_for('staff_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            message = 'Invalid username or password'
    return render_template('login.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'student')
        if username in users:
            message = 'Username already exists'
        else:
            users[username] = {'password': password, 'role': role}
            return redirect(url_for('login'))
    return render_template('register.html', message=message)


@app.route('/student_dashboard')
def student_dashboard():
    if 'username' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/courses')
def courses():
    if 'username' not in session: return redirect(url_for('login'))
    return "<h2>Manage Courses</h2><p>Course management system coming soon.</p><a href='/student_dashboard'>Back</a>"


@app.route('/progress')
def progress():
    if 'username' not in session: return redirect(url_for('login'))
    return "<h2>Academic Progress</h2><p>Grades and progress tracking coming soon.</p><a href='/student_dashboard'>Back</a>"


@app.route('/assignments')
def assignments():
    if 'username' not in session: return redirect(url_for('login'))
    return "<h2>Assignments</h2><p>Assignment submission portal coming soon.</p><a href='/student_dashboard'>Back</a>"


@app.route('/online-class')
def online_class():
    if 'username' not in session: return redirect(url_for('login'))
    return "<h2>Online Class</h2><p>Virtual classroom link coming soon.</p><a href='/student_dashboard'>Back</a>"


@app.route('/staff_dashboard')
def staff_dashboard():
    if 'username' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))
    return render_template('staff_dashboard.html', username=session['username'])


@app.route('/manage-courses')
def manage_courses():
    if 'username' not in session: return redirect(url_for('login'))
    return "<h2>Manage Courses</h2><p>Course administration system coming soon.</p><a href='/staff_dashboard'>Back</a>"


@app.route('/student-records')
def student_records():
    if 'username' not in session: return redirect(url_for('login'))
    return "<h2>Student Records</h2><p>Record management system coming soon.</p><a href='/staff_dashboard'>Back</a>"


@app.route('/gradebook')
def gradebook():
    if 'username' not in session: return redirect(url_for('login'))
    return "<h2>Faculty Gradebook</h2><p>Grade entry system coming soon.</p><a href='/staff_dashboard'>Back</a>"


@app.route('/department-meetings')
def dept_meetings():
    if 'username' not in session: return redirect(url_for('login'))
    return "<h2>Department Meetings</h2><p>Meeting schedule coming soon.</p><a href='/staff_dashboard'>Back</a>"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)