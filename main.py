from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory user storage (temporary)
users = {}


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('dashboard', username=username))
        else:
            message = 'Invalid username or password'
    return render_template('login.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            message = 'Username already exists'
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template('register.html', message=message)


@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('dashboard.html', username=username)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
