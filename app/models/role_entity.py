"""
ORM for Role table
"""

# from flask_security import RoleMixin
from app.main import db
from app.crud_mixin import CRUDMixin

ROLE_ADMIN = 'admin'
ROLE_TECHNICIAN = 'user'


class RoleEntity(db.Model, CRUDMixin):  # RoleMixin

    """ Stores possible user roles """
    __tablename__ = 'Role'

    id = db.Column("rolID", db.Integer, primary_key=True)
    name = db.Column("rolName", db.String(255), nullable=False, unique=True)
    description = db.Column("rolDescription", db.String(255), nullable=False)

    def __repr__(self):
        """ implements friendly representation """
        return "<RoleEntity (rolID: {0.id}, rolName: {0.name})>" \
            .format(self)
