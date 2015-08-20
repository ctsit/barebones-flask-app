"""
Goal: test insert/search user, role, user role
"""

from sqlalchemy.orm.exc import NoResultFound
from .base_test import BaseTestCase
from app.main import db
from app import utils

from app.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN
from app.models.user_entity import UserEntity
from app.models.role_entity import RoleEntity
from app.models.user_role_entity import UserRoleEntity
from datetime import datetime


class TestUserRole(BaseTestCase):

    """ test basic operations for User, Role, UserRole entities """

    def get_role(self, role):
        """ helper for creating roles """
        roles = {
            ROLE_ADMIN: RoleEntity(name=ROLE_ADMIN,
                                   description='role'),
            ROLE_TECHNICIAN: RoleEntity(name=ROLE_TECHNICIAN,
                                        description='role'),
        }
        return roles[role]

    def test_role(self):
        """ verify save and find operations """
        role_admin = self.get_role(ROLE_ADMIN)
        role_tech = self.get_role(ROLE_TECHNICIAN)

        db.session.add(role_admin)
        # before commit the primary key does not exist
        self.assertIsNone(role_admin.id)

        # after commit the primary key is generated
        db.session.commit()
        assert 1 == role_admin.id

        roles = RoleEntity.query.all()
        assert len(roles) == 1

        # test usage of CRUDMixin.get_by_id() and create()
        role_tech = RoleEntity.save(role_tech)
        assert 2 == role_tech.id

        ordered = RoleEntity.query.order_by(RoleEntity.name).all()
        # verify that we have two rows now
        assert 2 == len(ordered)

        # verify that the attribute is saved
        first = ordered[0]
        assert ROLE_ADMIN == first.name

        # verify that sorting worked
        first = RoleEntity.query.order_by(db.desc(RoleEntity.name)).first()
        assert ROLE_TECHNICIAN == first.name

    def test_user(self):
        """ verify save and find operations """
        added_date = datetime.today()
        access_end_date = utils.get_expiration_date(180)
        user = UserEntity.create(email="admin@example.com",
                                 first="",
                                 last="",
                                 minitial="",
                                 added_at=added_date,
                                 modified_at=added_date,
                                 access_expires_at=access_end_date)
        self.assertEqual(1, user.id)
        self.assertEqual("admin@example.com", user.email)

        with self.assertRaises(NoResultFound):
            UserEntity.query.filter_by(email="admin@example.com2").one()

        found = UserEntity.query.filter_by(email="admin@example.com").one()
        self.assertIsNotNone(found)

        # two unbound objects ...
        role_admin = self.get_role(ROLE_ADMIN)
        role_tech = self.get_role(ROLE_TECHNICIAN)

        # save them to the database...
        db.session.add(role_admin)
        db.session.add(role_tech)
        db.session.commit()

        saved_role = RoleEntity.query.filter_by(name=ROLE_ADMIN).one()
        self.assertEqual(1, saved_role.id)

        # ...then use them
        user.roles.append(role_admin)
        user.roles.append(role_tech)

        user_roles = UserRoleEntity.query.all()
        self.assertEqual(2, len(user_roles))

        user_role = UserRoleEntity.get_by_id(1)
        self.assertEqual(1, user_role.id)
        self.assertEqual(ROLE_ADMIN, user_role.role.name)

    def test_view_roles(self):
        """ @TODO: add test for viewing users """

        # from flask import url_for
        # response = self.client.post(url_for('/api/list_users'), data={})
        # self.assert_redirects(response, url_for(''))
