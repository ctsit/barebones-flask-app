"""
ORM for User table
"""

from datetime import datetime
from flask_login import UserMixin

# flask_security expands the flask_login UserMixin class with:
#   is_active(), get_auth_token, has_role()
from app.main import db
from app.crud_mixin import CRUDMixin
from app.models.role_entity import RoleEntity
from app.models.user_role_entity import UserRoleEntity
from app import utils


class UserEntity(db.Model, UserMixin, CRUDMixin):

    """ Stores the basic information about the user.
    Implements the functions as required by:
        https://flask-login.readthedocs.org/en/latest/
    """
    __tablename__ = 'User'

    id = db.Column("usrID", db.Integer, primary_key=True)
    email = db.Column("usrEmail", db.String(255), nullable=False, unique=True)
    first = db.Column("usrFirst", db.String(255), nullable=False)
    last = db.Column("usrLast", db.String(255), nullable=False)
    minitial = db.Column("usrMI", db.String(1), nullable=False)
    added_at = db.Column("usrAddedAt", db.DateTime, nullable=False,
                         server_default='0000-00-00 00:00:00')
    modified_at = db.Column("usrModifiedAt", db.TIMESTAMP, nullable=False)
    email_confirmed_at = db.Column("usrEmailConfirmedAt", db.DateTime,
                                   nullable=False,
                                   server_default='0000-00-00 00:00:00')
    active = db.Column("usrIsActive", db.Boolean(), nullable=False,
                       server_default='1')

    access_expires_at = db.Column("usrAccessExpiresAt", db.DateTime,
                                  nullable=False,
                                  server_default='0000-00-00 00:00:00')
    password_hash = db.Column("usrPasswordHash", db.String(255),
                              nullable=False, server_default='')

    # @OneToMany
    roles = db.relationship(RoleEntity,
                            secondary=UserRoleEntity.__tablename__,
                            backref=db.backref('users'),
                            lazy='dynamic')
    """
    `lazy` defines when SQLAlchemy will load the data from the:
        'select' (which is the default) means that SQLAlchemy will load the
        data as necessary in one go using a standard select statement.
    'joined' tells SQLAlchemy to load the relationship in the same query as the
        parent using a JOIN statement.
    'subquery' works like 'joined' but instead SQLAlchemy will use a subquery.
    'dynamic' is special and useful if you have may items. Instead of loading
        the items SQLAlchemy will return another query object which you can
        further refine before loading them items. This is usually what you want
        if you expect more than a handful of items for this relationship.
    """

    def is_active(self):
        """ An user can be blocked by setting a flag in the """
        return self.active

    def is_expired(self):
        """ An user can be blocked by setting expiration date to yesterday"""
        return self.access_expires_at < datetime.today()

    def is_anonymous(self):
        """ Flag instances of valid users """
        return False

    def is_authenticated(self):
        """ Returns True if the user is authenticated, i.e. they have provided
        valid credentials.
        (Only authenticated users will fulfill the criteria of login_required.)
        """
        return True

    def get_id(self):
        """ The id encrypted in the session """
        return unicode(self.id)

    def get_roles(self):
        """ Return text representation of user roles """
        return [role.name for role in self.roles]

    def get_name(self):
        """
        :rtype string
        :return concat(first, ' ', last)
        """
        return "{} {}".format(
            self.first.encode('utf-8'),
            self.last.encode('utf-8'))

    def get_email_verification_token(self, salt, secret):
        """
        :rtype string
        :return the email verification token stored in the
        """
        return utils.get_email_token(self.email, salt, secret)

    def serialize(self):
        """Return object data for jsonification"""
        return {
            'id': self.id,
            'email': self.email,
            'roles': [r.name for r in self.roles],
            'first': self.first,
            'last': self.last,
            'minitial': self.minitial,
            'is_active': True if self.active else False,
            'is_expired': True if self.is_expired() else False,
            'added_at': utils.localize_est_date(self.added_at),
            'email_confirmed_at':
                utils.localize_est_datetime(self.email_confirmed_at),
            'access_expires_at':
                utils.localize_est_datetime(self.access_expires_at)
        }

    def __repr__(self):
        return "<UserEntity (usrID: {0.id}, usrEmail: {0.email}, " \
               "usrIsActive: {0.active})>".format(self)
