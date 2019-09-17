from config import *
from datetime import datetime, timedelta
from models import Studentdata, authusers, delete_data, add_data, commit_changes

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
                add_data(new_task)
                commit_changes()
                return redirect('/sdata')
            except:
                return "THERE WAS A PROBLEM IN ENTERING DATA TO DATABASE"

        else:
            tasks = Studentdata.query.order_by(Studentdata.id).all()
            return render_template('sdata.html' , tasks=tasks)
    else:
        return "ERROR PLEASE LOGIN FIRST ", 401

@app.route('/delete/<int:id>')
def deletentry(id):
    task_delete = Studentdata.query.get_or_404(id)
    try:
        delete_data(task_delete)
        commit_changes()
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
            commit_changes()
            return redirect('/sdata')
        except:
            return "THere is some issue in updating the data"

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
