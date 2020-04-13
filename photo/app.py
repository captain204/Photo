from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_heroku import Heroku
from photo.models import db
from photo.views import photo_blueprint




def create_app(config_filename):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_filename)
    db.init_app(app)
    app.register_blueprint(photo_blueprint, url_prefix='/photo')
    migrate = Migrate(app, db)
    heroku = Heroku(app)
    return app


app = create_app('config')


