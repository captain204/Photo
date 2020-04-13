from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from photo.models import db
from photo.views import photo_blueprint



def create_app(settings_override=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py', silent=True)
    if settings_override:
        app.config.update(settings_override)

    db.init_app(app)
    app.register_blueprint(photo_blueprint, url_prefix='/photo')
    migrate = Migrate(app, db)
    return app


app = create_app('config')

