from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from requests import patch 
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_database(app):
    if not path.exists('Website/'+ DB_NAME):
        db.create_all(app=app)
        print('database created')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'AHAHAHAHAH AHAHHAAH'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    from .views import views
    from .auth import auth


    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from .models import User, Note
    
    with app.app_context():
        db.create_all()
    # db.create_all(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
