"""
Goal: set the environment for tests


Docs:
https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html

The only things you need to know compared to plain SQLAlchemy are:

SQLAlchemy gives you access to the following things:
 - all the functions and classes from sqlalchemy and sqlalchemy.orm
 - a preconfigured scoped session called session
 - the metadata
 - the engine
 - a SQLAlchemy.create_all() and SQLAlchemy.drop_all() methods to create and
    drop tables according to the models
 - a Model baseclass that is a configured declarative base
 - The Model declarative base class behaves like a regular Python class but has
    a query attribute attached that can be used to query the model
 - You have to commit the session, but you don't have to remove it at the end
    of the request, Flask-SQLAlchemy does that for you.
"""

from flask_testing import TestCase
from app.main import app, db, mail
from app import initializer
from config import MODE_TEST

class BaseTestCase(TestCase):

    """ Base class for all tests"""

    def create_app(self):
        """ override the default config with the test config """
        initializer.do_init(app, MODE_TEST)
        mail.init_app(app)
        return app

    def setUp(self):
        """ create all tables """
        db.create_all()

    def tearDown(self):
        """ remove all tables """
        db.session.remove()
        db.drop_all()
