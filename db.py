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

    return render_template('index.html')


@app.route('/redirect', methods=['GET','POST'])
def redirectTo():

    sel = request.form['selection']
    if sel == 'showall':
        cur = mysql.connection.cursor()
        t = (str(session['user']))
        cur.execute('''SELECT * FROM sample WHERE user='%s' ''' % t)
        entries = cur.fetchall()
        datas = []

        for entry in entries:
            dict = {
                'id' : int(entry[0]),
                'name': str(entry[1]),
                'place': str(entry[2])
            }
            datas.append(dict)


        return render_template('show.html', entries=datas)

    if sel == 'showone':
        return render_template('showone.html')
    #
    # if sel == edit:
    #     return render_template('edit.html')
    #
    if sel == 'add':
        return render_template('addone.html')

    if sel == 'login':
        return render_template('login.html')

    if sel == 'signup':
        return render_template('signup.html')



    return redirect(url_for('index'))

@app.route('/getone', methods=['POST'])
def showone():
    cur = mysql.connection.cursor()
    req_form = request.form
    t = (int(req_form['id']), str(req_form['name']), str(req_form['place']), session['user'])

    cur.execute('''SELECT * FROM sample WHERE id=%d AND name='%s' AND place='%s' AND user='%s' '''% t)
    entries = cur.fetchall()
    datas = []

    for entry in entries:
        dict = {
            'id' : int(entry[0]),
            'name': str(entry[1]),
            'place': str(entry[2])
        }
        datas.append(dict)

    # mysql.connection.commit()
    # flash('New entry was successfully posted')
    return render_template('show.html', entries=datas)



@app.route('/addone', methods=['POST'])
def add_entry():
    cur = mysql.connection.cursor()
    req_form = request.form
    t = (int(req_form['id']), str(req_form['name']), str(req_form['place']), session['user'])

    cur.execute('''INSERT INTO sample(id, name, place, user) VALUES (%d, '%s', '%s', '%s') ''' % t)

    mysql.connection.commit()
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        req_form = request.form
        t = (str(req_form['username']), str(req_form['password']))
        cur.execute('''SELECT * FROM users WHERE user='%s' AND password='%s' ''' % t)
        entries = cur.fetchall()



        if len(entries) == 0:
            error = 'Invalid username'

        else:
            session['logged_in'] = True
            session['user'] = str(req_form['username'])
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        req_form = request.form
        t = (str(req_form['username']), str(req_form['password']))
        cur.execute('''SELECT * FROM users WHERE user='%s' AND password='%s' ''' % t)
        entries = cur.fetchall()
        if len(entries) > 0:
            error = 'Duplicate username'
        else:
            cur.execute('''INSERT INTO users(user, password) VALUES('%s', '%s') ''' % t)
            mysql.connection.commit()
            session['logged_in'] = True
            session['user'] = str(req_form['username'])
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('signup.html', error=error)




@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug = True)
    # app.run(host = '0.0.0.0', debug=True)
