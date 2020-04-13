from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from photo.models import db
from photo.views import photo_blueprint


def create_app(photo.config):
    app = Flask(__name__)
    app.config.from_object(photo.config)
    db.init_app(app)
    app.register_blueprint(photo_blueprint, url_prefix='/photo')
    migrate = Migrate(app, db)
    return app


app = create_app('config')

