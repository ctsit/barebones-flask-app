"""
ORM for UserRole table
"""

from app.main import db
from app.crud_mixin import CRUDMixin


class UserRoleEntity(db.Model, CRUDMixin):
    """ Stores the user-role mapping """
    __tablename__ = 'UserRole'

    id = db.Column("urID", db.Integer, primary_key=True)
    user_id = db.Column("usrID", db.Integer, db.ForeignKey('User.usrID',
                        ondelete='CASCADE'), nullable=False)
    role_id = db.Column("rolID", db.Integer, db.ForeignKey('Role.rolID',
                        ondelete='CASCADE'), nullable=False)
    added_at = db.Column('urAddedAt', db.DateTime(), nullable=False,
                         server_default='0000-00-00 00:00:00')

    role = db.relationship('RoleEntity', uselist=False)
    user = db.relationship('UserEntity', uselist=False)

    def get_id(self):
        """ return the unicode of the primary key value """
        return unicode(self.id)

    def __repr__(self):
        return "<UserRoleEntity (\n\t" \
            "urID: {0.id}, \n\t" \
            " {0.user!r}, \n\t" \
            " {0.role!r}, \n" \
            " {0.added_at}, \n" \
            ")>".format(self)
