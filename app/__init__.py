from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from flask_migrate import Migrate
from flask_compress import Compress
from app.config import Config
import os

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
mail = Mail()
compress = Compress()
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    compress.init_app(app)
    
    from app.admin import admin
    from app.visitor import visitor
    from app.errors import error
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(visitor)
    app.register_blueprint(error)
    return app