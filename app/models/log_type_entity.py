"""
ORM for LogType table
"""
from app.crud_mixin import CRUDMixin
from app.main import db

LOG_TYPE_ACCOUNT_CREATED = 'account_created'
LOG_TYPE_LOGIN = 'login'
LOG_TYPE_LOGOUT = 'logout'
LOG_TYPE_LOGIN_ERROR = 'login_error'
LOG_TYPE_ACCOUNT_MODIFIED = 'account_modified'


class LogTypeEntity(db.Model, CRUDMixin):

    """ Stores types of logs """
    __tablename__ = 'LogType'

    id = db.Column('logtID', db.Integer, primary_key=True)
    type = db.Column('logtType', db.String(255), nullable=False)
    description = db.Column('logtDescription', db.Text, nullable=False)

    def __repr__(self):
        """ Return a friendly object representation """
        return ("<LogTypeEntity(id: {0.id}, "
                "logtType: {0.type}, "
                "logtDescription: {0.description})>"
                .format(self))
