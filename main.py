from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'university_secret_key'

# In-memory user storage
# Format: {'email': {'password': '...', 'role': '...', 'username': '...'}}
users = {
    'admin@spu.ac.za': {'password': 'admin123', 'role': 'staff', 'username': 'Admin Staff'},
    'student@spu.ac.za': {'password': 'password123', 'role': 'student', 'username': 'Student One'}
}

def get_role_from_email(email):
    # Staff emails usually end in @spu.ac.za (lecturers)
    # Student emails usually end in @student.spu.ac.za
    if email.endswith('@spu.ac.za') and not email.endswith('@student.spu.ac.za'):
        return 'staff'
    elif email.endswith('@student.spu.ac.za'):
        return 'student'
    return None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['email'] = email
            session['username'] = users[email]['username']
            session['role'] = users[email]['role']
            if session['role'] == 'staff':
                return redirect(url_for('staff_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            message = 'Invalid email or password'
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']
        username = request.form['username']
        
        role = get_role_from_email(email)
        
        if not role:
            message = 'Please use a valid university email (@spu.ac.za or @student.spu.ac.za)'
        elif email in users:
            message = 'Email already registered'
        else:
            users[email] = {'password': password, 'role': role, 'username': username}
            return redirect(url_for('login'))
    return render_template('register.html', message=message)

@app.route('/student_dashboard')
def student_dashboard():
    if 'email' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/staff_dashboard')
def staff_dashboard():
    if 'email' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))
    return render_template('staff_dashboard.html', username=session['username'])

@app.route('/courses')
def courses():
    if 'email' not in session: return redirect(url_for('login'))
    return "<h2>Manage Courses</h2><p>Course management system coming soon.</p><a href='/student_dashboard'>Back</a>"

@app.route('/progress')
def progress():
    if 'email' not in session: return redirect(url_for('login'))
    return "<h2>Academic Progress</h2><p>Grades and progress tracking coming soon.</p><a href='/student_dashboard'>Back</a>"

@app.route('/assignments')
def assignments():
    if 'email' not in session: return redirect(url_for('login'))
    return "<h2>Assignments</h2><p>Assignment submission portal coming soon.</p><a href='/student_dashboard'>Back</a>"

@app.route('/online-class')
def online_class():
    if 'email' not in session: return redirect(url_for('login'))
    return "<h2>Online Class</h2><p>Virtual classroom link coming soon.</p><a href='/student_dashboard'>Back</a>"

@app.route('/manage-courses')
def manage_courses():
    if 'email' not in session: return redirect(url_for('login'))
    return "<h2>Manage Courses</h2><p>Course administration system coming soon.</p><a href='/staff_dashboard'>Back</a>"

@app.route('/student-records')
def student_records():
    if 'email' not in session: return redirect(url_for('login'))
    return "<h2>Student Records</h2><p>Record management system coming soon.</p><a href='/staff_dashboard'>Back</a>"

@app.route('/gradebook')
def gradebook():
    if 'email' not in session: return redirect(url_for('login'))
    return "<h2>Faculty Gradebook</h2><p>Grade entry system coming soon.</p><a href='/staff_dashboard'>Back</a>"

@app.route('/department-meetings')
def dept_meetings():
    if 'email' not in session: return redirect(url_for('login'))
    return "<h2>Department Meetings</h2><p>Meeting schedule coming soon.</p><a href='/staff_dashboard'>Back</a>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)