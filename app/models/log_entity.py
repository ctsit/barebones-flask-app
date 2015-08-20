"""
ORM for app.Log table

@authors:
  Andrei Sura             <sura.andrei@gmail.com>
  Ruchi Vivek Desai       <ruchivdesai@gmail.com>
  Sanath Pasumarthy       <sanath@ufl.edu>
  Taeber Rapczak          <taeber@ufl.edu>
"""

import datetime
from app import utils
from app.crud_mixin import CRUDMixin
from app.main import app, db
from app.models.log_type_entity import LogTypeEntity
from app.models.web_session_entity import WebSessionEntity
from app.models.log_type_entity import \
    LOG_TYPE_ACCOUNT_CREATED, \
    LOG_TYPE_LOGIN, \
    LOG_TYPE_LOGOUT, \
    LOG_TYPE_LOGIN_ERROR, \
    LOG_TYPE_FILE_UPLOADED, \
    LOG_TYPE_FILE_DOWNLOADED, \
    LOG_TYPE_ACCOUNT_MODIFIED, \
    LOG_TYPE_REDCAP_SUBJECTS_IMPORTED, \
    LOG_TYPE_REDCAP_EVENTS_IMPORTED


class LogEntity(db.Model, CRUDMixin):

    """ Keep track of important user actions """
    __tablename__ = 'Log'

    id = db.Column('logID', db.Integer, primary_key=True)
    type_id = db.Column('logtID', db.Integer,
                        db.ForeignKey('LogType.logtID'),
                        nullable=False)
    web_session_id = db.Column('webID', db.Integer,
                               db.ForeignKey('WebSession.webID'),
                               nullable=False)
    date_time = db.Column('logDateTime', db.DateTime, nullable=False,
                          server_default='0000-00-00 00:00:00')
    details = db.Column('logDetails', db.Text, nullable=False)

    # @OneToOne
    log_type = db.relationship(LogTypeEntity, uselist=False, lazy='joined')
    web_session = db.relationship(WebSessionEntity, uselist=False,
                                  lazy='joined')

    @staticmethod
    def get_logs(per_page=25, page_num=1):
        """
        Helper for formating the event details
        """
        def item_from_entity(entity):
            return {
                'id': entity.id,
                'user_email': entity.web_session.user.email,
                'type': entity.log_type.type,
                'details': entity.details,
                'web_session_ip': entity.web_session.ip,
                'date_time': utils.localize_est_datetime(entity.date_time),
            }

        pagination = LogEntity.query.paginate(page_num, per_page, False)
        items = map(item_from_entity, pagination.items)
        return items, pagination.pages

    @staticmethod
    def _log(log_type, session_id, details=''):
        """ Helper for logging """
        logt = LogTypeEntity.query.filter_by(type=log_type).first()
        if logt is None:
            app.logger.error("Developer error. Invalid log type: {}"
                             .format(log_type))
            return

        web_session = WebSessionEntity.get_by_session_id(session_id)
        if web_session is None:
            app.logger.error("Developer error. Invalid session id: {}"
                             .format(session_id))
            return

        LogEntity.create(log_type=logt,
                         date_time=datetime.datetime.now(),
                         details=details,
                         web_session=web_session)

    @staticmethod
    def account_created(session_id, details=''):
        """ Log account creation """
        LogEntity._log(LOG_TYPE_ACCOUNT_CREATED, session_id, details)

    @staticmethod
    def login(session_id, details=''):
        """ Log successful login """
        LogEntity._log(LOG_TYPE_LOGIN, session_id, details)

    @staticmethod
    def logout(session_id, details=''):
        """ Log logout click """
        LogEntity._log(LOG_TYPE_LOGOUT, session_id, details)

    @staticmethod
    def login_error(session_id, details=''):
        """ Log failed login """
        LogEntity._log(LOG_TYPE_LOGIN_ERROR, session_id, details)

    @staticmethod
    def file_uploaded(session_id, details=''):
        """ Log file upload """
        LogEntity._log(LOG_TYPE_FILE_UPLOADED, session_id, details)

    @staticmethod
    def file_downloaded(session_id, details=''):
        """ Log file download """
        LogEntity._log(LOG_TYPE_FILE_DOWNLOADED, session_id, details)

    @staticmethod
    def account_modified(session_id, details=''):
        """ Log account changes """
        LogEntity._log(LOG_TYPE_ACCOUNT_MODIFIED, session_id, details)

    @staticmethod
    def redcap_subjects_imported(session_id, details=''):
        """ Log it """
        LogEntity._log(LOG_TYPE_REDCAP_SUBJECTS_IMPORTED, session_id, details)

    @staticmethod
    def redcap_events_imported(session_id, details=''):
        """ Log it """
        LogEntity._log(LOG_TYPE_REDCAP_EVENTS_IMPORTED, session_id, details)

    def __repr__(self):
        """ Return a friendly object representation """
        return "<LogEntity(logID: {0.id}, "\
            "logtID: {0.type_id}" \
            "webID: {0.web_session_id}, "\
            "date_time: {0.date_time})>".format(self)
