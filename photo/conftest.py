import pytest
from app import create_app
from models import db
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from views import photo_blueprint


@pytest.fixture
def application():
    # Beggining of Setup code
    app = create_app('test_config')
    with app.app_context():   
        db.create_all()
        # End of Setup code
        # The test will start running here
        yield app
        # The test finished running here
        # Beginning of Teardown code
        db.session.remove()
        db.drop_all()
        # End of Teardown code


@pytest.fixture
def client(application):
    return application.test_client()

