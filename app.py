from flask import Flask, Blueprint

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
    return "<h1>Homepage</h1>"


@auth.route('/login')
def login():
    return "<h1>Login</h1>"


@auth.route('/register')
def register():
    return "<h1>Register</h1>"


@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"
