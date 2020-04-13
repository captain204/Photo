import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI ="postgres://csjyzpizvsrcyz:322561b75a2d80983effbbee73d860c7649f0a8de3887588afe3572c0f8f3fa1@ec2-54-152-175-141.compute-1.amazonaws.com:5432/d19el56a2rq7pg" 
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


PAGINATION_PAGE_SIZE = 4
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
