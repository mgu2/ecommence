from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_mysqldb import MySQL




app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '390819GMXa!'
app.config['MYSQL_DB'] = 'sampledatabase'
app.config['MYSQL_HOST'] = 'localhost'
app.secret_key = 'gmx'

mysql.init_app(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT id, name, place FROM sample''')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():

    cur = mysql.connection.cursor()
    req_form = request.form
    t = (str(req_form['id']), str(req_form['name']), str(req_form['place']))
    print t
    cur.execute('INSERT INTO sample (id, name, place) VALUES (%s, %s, %s)', t)


    mysql.connection.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)
#
#
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
# return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
