import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
#SQLALCHEMY_DATABASE_URI ="postgresql:///photodb"
from flask_heroku import Heroku
heroku = Heroku(app) 
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


PAGINATION_PAGE_SIZE = 4
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
