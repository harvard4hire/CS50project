"""
 scripts.py
 
 Computer Science 50
 Final Project
 Harvard Skills

 Global JavaScript.
 
"""

### CINDY ######################################################################

import sqlite3

from contextlib import closing

DATABASE = '/tmp/scripts.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


from flask import *
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
        
@app.before_request
def before_request():
    g.db = connect_db()
    
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


import os
os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

"""# index or homepage
@app.route('/')
def index():
    return render_template('home.html')

# login form
@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != app.config['EMAIL']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return render_template('home.html')
    return render_template('loginform.html', error=error)'''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session['logged_in'] = False
    return render_template('home.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'GET':
        return render_template('register.html')
    else:
        if request.form['first'] == "" or request.form['last'] == "":
            return "You must provide a username" #TODO later, make it alert instead of return
        elif request.form['email'] == "":
            return "Please enter an email"
        elif request.form['password'] == "":
            return "You must provide a password"
        elif request.form['confirmation'] == "":
            return "Please type your password again"
        elif request.form['confirmation'] != request.form['password']:
            return "Your passwords do not match"
        else:
            '''g.db.execute('insert into entries (first, last, email, password) values (?, ?, ?, ?)',
                [request.form['first'], request.form['last'], request.form['email'],
                os.urandom(request.form['password'])])
            g.db.commit()'''
            return "You have registered!"

@app.route('/profile/')
@app.route('/profile/<userid>')
def profile(userid=None):
    error = None
    if 'userid' in session:
        return render_template('profile.html', title = 'Your Profile', userid = userid)
    else:
        return render_template('profile.html')
        
@app.route('/newpost/')
@app.route('/newpost/<userid>/<jobid>')
def newpost(userid=None, jobid=None):
    error = None
    if 'userid' in session:
        return render_template('newpost.html', userid = userid, jobid = jobid)
    else:
        return render_template('newpost.html')
"""

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    else:
        db = get_db()
        db.execute('insert into entries (title, text) values (?, ?)',
                     [request.form['title'], request.form['text']])
        db.commit() == True
        flash('New entry was successfully posted')
        return render_template('show_entries.html')
    
   
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != 'admin':
            return 'Invalid username'
        elif request.form['hash'] != 'default':
            return 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return render_template('show_entries.html')
    else:
        return render_template('login.html', error=error)
    
@app.route('/')
def show_entries():
    return render_template('layout.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return render_template('layout.html')

###############################################################################

if __name__ == '__main__':
    app.run()
    
    
    
    
    
    
