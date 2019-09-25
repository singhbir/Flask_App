from flask import Flask, render_template, url_for, request, redirect, flash, session, g,jsonify
from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token, jwt_required

from models import Studentdata, authusers, delete_data, add_data, commit_changes,execute




def test_1():
    if request.method == 'GET':
        return jsonify(
            result="thanks for sending GET request"
        )

def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        token = True
        task = authusers(name=name, email=email, password=password, token=token, new_dt=datetime.now()+timedelta(minutes=1))


        try:
            add_data(task)
            commit_changes()
            #redirect('/mainlogin')
            return jsonify(
                result="Thanks for signup",
                name=name,
                email=email
                )
        except:
            return "sorry cannot save your data", 401
    else:
        return render_template('login.html')

def mlogin():
    if request.method == 'POST':
        session.pop('user', None)
        cemail = request.form['lemail']
        cpassword = request.form['lpassword']
        result_p = execute(cemail)
        passw = [row[0] for row in result_p]
        if cpassword == passw[0]:
            session['user'] = request.form['lemail']
            access_token = create_access_token(identity=cemail)


            return jsonify(
                result="LOGIN SUCCESSFUL",
                token=access_token
            )
            #redirect('/sdata')
        else:
             return jsonify(
                 result="PLEASE CHECK YOUR EMAIL ID OR PASSWORD"
             )
             #render_template('mainlogin.html')
    else:
        return jsonify(
            error="CHECK YOUR SENDING METHOD"
        )

@jwt_required
def hello_world():
    if request.method == 'POST':
        sname = request.form['sname']
        tname = request.form['tname']
        new_task = Studentdata(name=sname, teacher=tname)

        try:
            add_data(new_task)
            commit_changes()
            return jsonify(
                        name=sname,
                        teacher=tname,
                        result="DATA SAVED SUCCESSFULLY"
                )
                    #redirect('/sdata')
        except:
            return jsonify(name=sname,
                            teacher=tname,
                             result="DB ERROR")
    else:
        return jsonify(result="request method get")

@jwt_required
def deletentry(id):
    task_delete = Studentdata.query.get_or_404(id)
    try:
        delete_data(task_delete)
        commit_changes()
        return jsonify(result="deleted successfully")
        #redirect('/sdata')
    except:
        return jsonify(result='not deleted')

@jwt_required
def updatentry(id):
    task_update = Studentdata.query.get_or_404(id)

    if request.method == 'POST':
        task_update.name = request.form['sname']
        task_update.teacher = request.form['tname']

        try:
            commit_changes()
            return jsonify(
                new_name=task_update.name,
                new_teacher_name=task_update.teacher,
                result="successfully update"
            )
            #redirect('/sdata')
        except:
            return jsonify(result="commit issue")

    else:
        return jsonify(result="please check sending method")
        #render_template('update.html', task=task_update)



