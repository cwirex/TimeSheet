import json
import re
from os import path
from datetime import datetime

from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__, )
auth = Blueprint('auth', __name__, )
DB_NAME = "database.db"
db = SQLAlchemy()
loginMenager = LoginManager()

from models import User, Task, Client


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'khjGBkYT675ivhgj76$IF!7x56'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    if not path.exists(DB_NAME):
        db.create_all(app=app)

    loginMenager.login_view = 'auth.login'
    loginMenager.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app


@loginMenager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    clients = {}
    try:
        for client in db.session.query(Client).order_by(Client.id):
            clients[client.id] = client
    except:
        flash('Query clients failed.', category='error')
    return render_template("home.html", user=current_user, clients=clients)


@views.route('/client-manager', methods=['GET', 'POST'])
@login_required
def client_manager():
    if request.method == 'POST':
        data = request.form
        phone = data['phone']
        first_name = data['first_name']
        last_name = data['last_name']
        if len(first_name) < 3 and len(last_name) < 3:
            flash('Name must be at least 3 characters long.', category='error')
        else:
            client = Client(phone=phone, first_name=first_name, last_name=last_name)
            try:
                db.session.add(client)
                db.session.commit()
                flash('New task created successfully!')
            except:
                flash('New task cannot be created.')
    return render_template("client.html", user=current_user)


@views.route('/task-creator', methods=['GET', 'POST'])
@login_required
def task_creator():
    if request.method == 'POST':
        data = request.form
        title = data['title']
        details = data['details']
        time_start = data['time_start']
        client_id = int(data['select_client'])
        if time_start:
            time_start = datetime.strptime(time_start, '%Y-%m-%dT%H:%M')
        time_end = data['time_end']
        if time_end:
            time_end = datetime.strptime(time_end, '%H:%M').time()
        if len(title) < 3:
            flash('Title must be at least 3 characters.', category='error')
        else:
            user_id = current_user.id
            task = Task(user_id=user_id, title=title, details=details)
            if time_start:
                task.time_start = time_start
            if time_end:
                task.time_end = time_end
            if client_id != 0:
                task.client_id = client_id
            try:
                db.session.add(task)
                db.session.commit()
                flash('New task created successfully!', category='success')
            except:
                flash('New task cannot be created.')
    clients = []
    try:
        clients = db.session.query(Client).order_by(Client.last_name)
    except:
        flash('Query clients failed.', category='error')
    return render_template("task.html", user=current_user, clients=clients)


@views.route('/delete-task', methods=['POST'])
def delete_task():
    data = json.loads(request.data)
    task_id = data['taskId']
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            try:
                db.session.delete(task)
                db.session.commit()
                return jsonify({})
            except:
                flash('Failed to delete the task', category='error')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        login = data['login']
        password = data['password']
        user = User.query.filter_by(email=login).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Username not found.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']
        name = data['name']
        if User.query.filter_by(email=email).first():
            flash('Email already taken.', category='error')
        elif password1 != password2:
            flash('Passwords does not match.', category='error')
        elif len(password1) < 6:
            flash('Password too short.', category='error')
        elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            flash('Email is not valid.', category='error')
        else:
            if name:
                user = User(email=email, password=generate_password_hash(password1), name=name)
            else:
                user = User(email=email, password=generate_password_hash(password1))
            try:
                db.session.add(user)
                db.session.commit()
                flash('Account created', category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            except:
                flash('Account not created...')

    return render_template("register.html", user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
