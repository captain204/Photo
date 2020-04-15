from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_heroku import Heroku
from photo.models import db
from photo.views import photo_blueprint
from flasgger import Swagger


template = {
  "swagger": "2.0",
  "info": {
    "title": "Photo API",
    "description": "API for saving links to favourite user photos",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "nurudeenakindele8@gmail.com",
      "url": "www.me.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "host": "favouritephotoapi.herokuapp.com",  # overrides localhost:500
  "basePath": "/photo/",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}



def create_app(config_filename):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_filename)
    db.init_app(app)
    app.register_blueprint(photo_blueprint, url_prefix='/photo')
    migrate = Migrate(app, db)
    #heroku = Heroku(app)
    swagger = Swagger(app,template=template)
    return app


app = create_app('config')


