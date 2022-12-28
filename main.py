import numpy as np
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import datetime
import FDataBase
from FDataBase import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import psycopg2
import hashlib
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = psycopg2.connect(
    database="musicsoul_db",
    user="postgres",
    password="evil",
    host="localhost",
    port="5432"
)
con.autocommit = True
print("Database opened successfully")


@app.route('/')
def choose():
    return render_template('main_choose.html')


@app.route('/a_form', methods=['GET', 'POST'])
def a_form():
    cursor = con.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        result = hashlib.md5(password.encode())
        password_rs = result.hexdigest()
        cursor.execute('SELECT * FROM staff WHERE staff_login = %s', (username,))
        account = cursor.fetchone()
        session["name"] = account[1]
        session["id"] = account[0]
        session["pos"] = account[6]


        if (account[5] == password_rs and account[4] == username and account[6] == 2):
            return render_template('workplace_a.html')

        else:
            return render_template('main_choose.html')

    return render_template('a_form.html')


@app.route('/m_form', methods=['GET', 'POST'])
def m_form():
    cursor = con.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        result = hashlib.md5(password.encode())
        password_rs = result.hexdigest()
        cursor.execute('SELECT * FROM staff WHERE staff_login = %s', (username,))
        account = cursor.fetchone()
        session["name"] = account[1]
        session["id"] = account[0]

        if (account[5] == password_rs and account[4] == username and account[6] == 1):
            return render_template('workplace_m.html')
        else:
            return render_template('main_choose.html')

    return render_template('m_form.html')


@app.route('/workplace_a')
def workplace_a():
    return render_template('workplace_a.html')


@app.route('/workplace_m')
def workplace_m():
    if session.get("name"):
        return render_template('workplace_m.html')


@app.route('/show_client')
def show_client():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM client')
    account = cursor.fetchall()
    n = len(account)
    return render_template('show_client.html', account=account, n=n)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    cursor = con.cursor()
    if request.method == 'POST' and 'name' in request.form and 'login' in request.form and 'password' in request.form \
            and 'phone' in request.form and 'email' in request.form and 'role' in request.form:
        name = request.form['name']
        login = request.form['login']
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        role = request.form['role']
        FDataBase.addUser(name, login, password, phone, email, role, con)
        return render_template('workplace_m.html')
    return render_template('create_user.html')


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    cursor = con.cursor()
    if request.method == 'POST' and 'fin_date' in request.form and 'task_desc' in request.form \
            and 'cont_id' in request.form and 'executor' in request.form and 'client' in request.form and 'priority_num' in request.form:
        finish = request.form['fin_date']
        desc = (request.form['task_desc'])
        contract = (request.form['cont_id'])
        author = session.get("id")
        executor = (request.form['executor'])
        client = (request.form['client'])
        priority = (request.form['priority_num'])
        date_time_obj = datetime.datetime.strptime(finish, '%Y-%m-%d')
        finish = date_time_obj.date()
        FDataBase.addtask(finish, desc, contract, author, executor, client, priority, con)
        return render_template('workplace_m.html')
    return render_template('add_task.html')


@app.route('/update_task', methods=['GET', 'POST'])
def update_task():
    cursor = con.cursor()
    if request.method == 'POST' and 'id' in request.form and 'column' in request.form and 'after' in request.form:
        id_task = request.form['id']
        column = request.form['column']
        after = request.form['after']
        if (column == "finish_date"):
            cursor.execute('UPDATE task SET finish_date = %s WHERE task_id = %s', (after, id_task))
            return render_template('workplace_m.html')
        elif (column == "task_description"):
            cursor.execute('UPDATE task SET task_description = %s WHERE task_id = %s', (after, id_task))
            return render_template('workplace_m.html')
        elif (column == "task_status"):
            cursor.execute('UPDATE task SET task_status = %s WHERE task_id = %s', (after, id_task))
            return render_template('workplace_m.html')
        elif (column == "executor_id"):
            cursor.execute('UPDATE task SET executor_id = %s WHERE task_id = %s', (after, id_task))
            return render_template('workplace_m.html')
        elif (column == "priority"):
            cursor.execute('UPDATE task SET priority = %s WHERE task_id = %s', (after, id_task))
            return render_template('workplace_m.html')
        else:
            flash('You try to change wrong column, choose one of this: finish_date, task_description, task_status, executor_id, priority')
    return render_template('update_task.html')


@app.route('/update_client', methods=['GET', 'POST'])
def update_client():
    cursor = con.cursor()
    if request.method == 'POST' and 'id' in request.form and 'column' in request.form and 'after' in request.form:
        id_client = request.form['id']
        column = request.form['column']
        after = request.form['after']
        if (column == "client_phone"):
            cursor.execute('UPDATE client SET client_phone = %s WHERE client_id = %s', (after, id_client))
            return render_template('workplace_m.html')
        elif (column == "client_email"):
            cursor.execute('UPDATE client SET client_email = %s WHERE client_id = %s', (after, id_client))
            return render_template('workplace_m.html')
        elif (column == "client_postal_address"):
            cursor.execute('UPDATE client SET client_postal_address = %s WHERE client_id = %s', (after, id_client))
            return render_template('workplace_m.html')
        elif (column == "client_city"):
            cursor.execute('UPDATE client SET client_city = %s WHERE client_id = %s', (after, id_client))
            return render_template('workplace_m.html')
        else:
            flash('You try to change wrong column, choose one of this: client_city, client_postal_address, client_email, client_phone')
    return render_template('update_client.html')


@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    cursor = con.cursor()
    if request.method == 'POST' and 'id_w' in request.form:
        id = request.form['id']
        id_m = session.get("id")
        cursor.execute("CALL dismissal(%s,%s)", (id, id_m))
    return render_template('transaction.html')


@app.route('/find_client', methods=['GET', 'POST'])
def find_client():
    cursor = con.cursor()
    if request.method == 'POST' or 'name' in request.form or 'city' in request.form or 'id' in request.form:
        name = request.form['name']
        city = request.form['city']
        id = request.form['id']

        if name:
            cursor.execute('SELECT * FROM client WHERE client_name = %s', (name,))
            account = cursor.fetchall()
            return render_template('find_client.html', account=account)
        elif city:
            cursor.execute('SELECT * FROM client WHERE client_city = %s', (city,))
            account1 = cursor.fetchall()
            return render_template('find_client.html', account=account1)
        elif id:
            cursor.execute('SELECT * FROM client WHERE client_id = %s', (id,))
            account2 = cursor.fetchall()
            return render_template('find_client.html', account=account2)
    return render_template('find_client.html')


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    cursor = con.cursor()
    if request.method == 'POST' and 'id' in request.form and 'name' in request.form \
            and 'phone' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'comp_id' in request.form:
        id = request.form['id']
        name = (request.form['name'])
        phone = (request.form['phone'])
        email = (request.form['email'])
        address = (request.form['address'])
        city = (request.form['city'])
        comp_id = (request.form['comp_id'])
        cursor.execute("CALL new_client(%s,%s,%s,%s,%s,%s,%s)", (id, name, phone, email, address, city, comp_id))
        return render_template('workplace_m.html')
    return render_template('add_client.html')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    cursor = con.cursor()
    if request.method == 'POST' and 'id' in request.form and 'name' in request.form \
            and 'desc' in request.form and 'price' in request.form:
        id = request.form['id']
        name = (request.form['name'])
        desc = (request.form['desc'])
        price = (request.form['price'])
        cursor.execute("CALL new_product(%s,%s,%s,%s)", (id, name, desc, price))
        if session["pos"] == 1:
            return render_template('workplace_m.html')
        elif session["pos"] == 2:
            return render_template('workplace_a.html')
    return render_template('add_product.html')


@app.route('/add_contract', methods=['GET', 'POST'])
def add_contract():
    cursor = con.cursor()
    if request.method == 'POST' and 'id' in request.form and 'desc' in request.form \
            and 'start' in request.form and 'finish' in request.form and 'price' in request.form and 'address' in request.form and 'client' in request.form and 'product' in request.form:
        id = request.form['id']
        desc = (request.form['desc'])
        start = (request.form['start'])
        finish = (request.form['finish'])
        price = (request.form['price'])
        address = (request.form['address'])
        client = (request.form['client'])
        product = (request.form['product'])
        cursor.execute("CALL new_product(%s,%s,%s,%s,%s,%s,%s,%s)", (id, desc, start, finish, price, address, client, product))
        return render_template('workplace_m.html')
    return render_template('add_contract.html')


@app.route('/uncomp_task')
def uncomp_task():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM not_done_task')
    account = cursor.fetchall()
    n = len(account)
    return render_template('uncomp_task.html', account=account, n=n)


@app.route('/sel_prod')
def sel_prod():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM product')
    account = cursor.fetchall()
    n = len(account)
    return render_template('sel_prod.html', account=account, n=n)


@app.route('/sel_cont')
def sel_cont():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM contract')
    account = cursor.fetchall()
    n = len(account)
    print(n)
    return render_template('sel_cont.html', account=account, n=n)


@app.route('/sel_staff')
def sel_staff():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM staff')
    account = cursor.fetchall()
    n = len(account)
    print(n)
    return render_template('sel_staff.html', account=account, n=n)


@app.route('/sel_m_task', methods=['GET', 'POST'])
def sel_m_task():
    cursor = con.cursor()
    id_m = session.get("id")
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
        if name == 'author_id':
            cursor.execute('SELECT * FROM task WHERE author_id = %s', ([id_m]))
            account = cursor.fetchall()
            n = len(account)
            return render_template('sel_m_task1.html', account=account, n=n)
        elif name == 'executor_id':
            cursor.execute('SELECT * FROM task WHERE executor_id = %s', ([id_m]))
            account = cursor.fetchall()
            n = len(account)
            return render_template('sel_m_task1.html', account=account, n=n)
    return render_template('sel_m_task.html')


@app.route('/sel_a_task')
def sel_a_task():
    cursor = con.cursor()
    id = session.get("id")
    cursor.execute('SELECT * FROM task WHERE executor_id = %s', ([id]))
    account = cursor.fetchall()
    n = len(account)
    return render_template('sel_a_task.html', account=account, n=n)


@app.route('/death_tab')
def death_tab():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM not_done_task')
    account = cursor.fetchall()
    n = len(account)
    return render_template('death_tab.html', account=account, n=n)



if __name__ == '__main__':
    app.run()
