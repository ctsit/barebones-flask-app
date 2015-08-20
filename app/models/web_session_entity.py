"""
ORM for WebSession table
"""
import datetime
from app.crud_mixin import CRUDMixin
from app.models.user_agent_entity import UserAgentEntity
from app.models.user_entity import UserEntity
from app.main import db


class WebSessionEntity(db.Model, CRUDMixin):
    """Store web session details"""
    __tablename__ = 'WebSession'

    id = db.Column('webID', db.Integer, primary_key=True)
    session_id = db.Column('webSessID', db.String(255), nullable=False,
                           default='')
    user_id = db.Column('usrID', db.Integer,
                        db.ForeignKey('User.usrID'),
                        nullable=False,
                        default=0)
    ip = db.Column('webIP', db.String(15), nullable=False, default='')
    date_time = db.Column('webDateTime', db.DateTime, nullable=False,
                          default=datetime.datetime(datetime.MINYEAR, 1, 1))
    user_agent_id = db.Column('uaID', db.Integer,
                              db.ForeignKey('UserAgent.uaID'),
                              nullable=False)
    # @OneToMany
    user_agent = db.relationship(UserAgentEntity, lazy='joined')
    user = db.relationship(UserEntity, lazy='joined')

    @staticmethod
    def get_by_session_id(session_id):
        """ Search helper: WHERE webSessID = ???"""
        return WebSessionEntity.query.filter_by(session_id=session_id).first()

    def __repr__(self):
        """ Return a friendly object representation """
        return "<WebSessionEntity (webID: '{0.id}', webSessID: {0.session_id},"\
               " usrID: {0.user_id}, webIP: {0.ip})>".format(self)
