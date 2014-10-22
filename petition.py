from flask import Flask, render_template, flash, redirect, url_for, session
from flask_login import LoginManager, login_required, request, login_user
import MySQLdb

login_manager = LoginManager()
app = Flask(__name__)
app.debug = True
login_manager.init(app)

db = MySQLdb.connect(host = 'localhost',
                     user = 'Xiaoyu Chen',
                     passwd = "petitions",
                     db = "petitions")

cur = db.cursor()

@app.route('/')
def show_main_page():
    #substitute the following file name with your template file name
    return render_template('PETITION_TEMPLATE.html')

@app.route('/petitions')
@login_required
def show_petitions():
    petitions_name = []
    petitions_description = []
    petitions_start_date = []
    petitions_end_date = []
    cur.execute('select * from petitions')
    for p_name in cur[2]:
        petitions_name.extend(p_name)

    for p_descript in cur[3]:
        petitions_description.extend(p_descript)

    for p_start in cur[4]:
        petitions_start_date.extend(p_start)

    for p_end in cur(5):
        petitions_end_date.extend(p_end)

    posts_info = [petitions_name, petitions_description, petitions_start_date, petitions_end_date]
    return render_template('PETITION_TEMPLATE.html', posts_info = posts_info)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_petitions'))

    return render_template('login.html', error=error)

app.run()
