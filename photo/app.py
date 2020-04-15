from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_heroku import Heroku
from photo.models import db
from photo.views import photo_blueprint
from flasgger import Swagger
template= {
    "swagger": "3.0",
    "openapi": "3.0.0",
    "info": {
        "title": "Photo App",
        "version": "0.0.1",
    },
    "components": {
      "schemas": {
        "User": {
          "properties": {
            "name": {
              "type": "string"
            },
            "email": {
              "type": "string"
            },
            "password": {
              "type": "string"
            }
          }
        },
        "Photo":{
          "properties":{
            "link":{
              "type":"string"
            },
            "description":{
              "type":"string"
            },
            "photo_category":{
              "type":"string"
            }
          }
        },
        "Category":{
          "properties":{
            "name":{
              "type":"string"
            }
          }
        }
      }
    }
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


