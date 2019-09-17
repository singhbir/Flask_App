from flask import Flask, render_template, url_for, request, redirect, flash, session,g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key="BIRSINGH"
db = SQLAlchemy(app)

email=""

class Studentdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    teacher = db.Column(db.String(200))

    def __repr__(self):
        return '<Task %r>' % self.id

class authusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String())
    token = db.Column(db.String(200), default=False)
    new_dt = db.Column(db.DateTime, default=datetime.now())


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        token = True
        task = authusers(name=name, email=email, password=password, token=token, new_dt=datetime.now()+timedelta(minutes=1))


        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/mainlogin')
        except:
            return "sorry cannot save your data", 401
    else:
        return render_template('login.html')

@app.route('/mainlogin', methods=['GET' , 'POST'])
def mlogin():
    if request.method == 'POST':
        session.pop('user', None)
        cemail = request.form['lemail']
        cpassword = request.form['lpassword']
        result_p = db.engine.execute(f"select password from authusers where email = '{cemail}'")
        passw = [row[0] for row in result_p]
        if cpassword == passw[0]:
            session['user'] = request.form['lemail']
            return redirect('/sdata')
        else:
             return render_template('mainlogin.html')
    else:
        return render_template('mainlogin.html')


@app.route('/sdata/', methods=['GET', 'POST'])
def hello_world():
    if g.user:
        if request.method == 'POST':
            sname = request.form['sname']
            tname = request.form['tname']
            new_task = Studentdata(name=sname, teacher=tname)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/sdata')
            except:
                return "THERE WAS A PROBLEM IN ENTERING DATA TO DATABASE"

        else:
            tasks = Studentdata.query.order_by(Studentdata.id).all()
            return render_template('sdata.html' , tasks=tasks)
    else:
        flash("LOGIN FIRST PLEASE")
        return "ERROR PLEASE LOGIN FIRST " , 401

@app.route('/delete/<int:id>')
def deletentry(id):
    task_delete = Studentdata.query.get_or_404(id)
    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/sdata')
    except:
        return 'There was a problem in deleting your data'

@app.route('/update/<int:id>', methods=['GET','POST'])
def updatentry(id):
    task_update = Studentdata.query.get_or_404(id)

    if request.method == 'POST':
        task_update.name = request.form['sname']
        task_update.teacher = request.form['tname']

        try:
            db.session.commit()
            return redirect('/sdata')
        except:
            return "THere is some issue in deleting the data"

    else:
        return render_template('update.html', task=task_update)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user', None)
    return redirect('/mainlogin')


if __name__ == '__main__':
    app.run(debug=True)
