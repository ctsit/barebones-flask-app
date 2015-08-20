"""
ORM for UserAgent table
"""
from app.crud_mixin import CRUDMixin
from app.main import db


class UserAgentEntity(db.Model, CRUDMixin):

    """ Store types of browsers """
    __tablename__ = 'UserAgent'

    id = db.Column('uaID', db.Integer, primary_key=True)
    user_agent = db.Column('uaUserAgent', db.String(255), nullable=False,
                           default='')
    hash = db.Column('uaHash', db.String(255), nullable=False)
    platform = db.Column('uaPlatform', db.String(255), nullable=False)
    browser = db.Column('uaBrowser', db.String(255), nullable=False)
    version = db.Column('uaVersion', db.String(255), nullable=False)
    language = db.Column('uaLanguage', db.String(255), nullable=False)

    @staticmethod
    def get_by_hash(hash):
        """ Search helper: WHERE uaHash = ???"""
        return UserAgentEntity.query.filter_by(hash=hash).first()

    def __repr__(self):
        """ Return a friendly object representation """
        return "<UserAgentEntity (uaID: '{0.id}', uaHash: {0.hash},"\
               " uaBrowser: {0.browser}, uaVersion: {0.version})>".format(self)
