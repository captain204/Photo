import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_DATABASE_URI ="postgresql:///photodb" 
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///db.photo_db"
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'db.photo_db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


PAGINATION_PAGE_SIZE = 4
PAGINATION_PAGE_ARGUMENT_NAME = 'page'


	