from flask import Flask, Blueprint, render_template

views = Blueprint('views', __name__, )
auth = Blueprint('auth', __name__, )


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'khjGBkYT675ivhgj76$IF!7x56'
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app


@views.route('/')
def home():
    return render_template("home.html")


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/register')
def register():
    return render_template("register.html")


@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"
