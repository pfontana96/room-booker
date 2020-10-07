from flask import Flask
from flask_login import LoginManager
from pathlib import Path

from project.auth import auth as auth_blueprint
from project.main import main as main_blueprint
from project.models import db, User

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    rep_path = Path(__file__).resolve().parent.parent # directorio room-booker
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(rep_path.joinpath('data/db.sqlite'))

    db.init_app(app)


    # Loader del user
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
