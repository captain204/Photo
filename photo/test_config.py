import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI ="postgresql:///test_photodb" 
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


PAGINATION_PAGE_SIZE = 4
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
# Enable the TESTING flag
TESTING = True
# Disable CSRF protection in the testing configuration
WTF_CSRF_ENABLED = False
# Necessary for flask.url_for to build the URLs
SERVER_NAME="127.0.0.1"

