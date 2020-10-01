from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .auth import auth as auth_blueprint
from .main import main as main_blueprint

# Init db
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
