"""
Goal: Extend the base test class by inserting samle rows in the database

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

from datetime import datetime
from .base_test import BaseTestCase
from app import utils
from app.main import db

from app.models.role_entity import ROLE_ADMIN, ROLE_TECHNICIAN
from app.models.user_entity import UserEntity
from app.models.role_entity import RoleEntity
from app.models.log_type_entity import LogTypeEntity
from app.models.user_agent_entity import UserAgentEntity
from app.models.log_type_entity import LOG_TYPE_LOGIN, LOG_TYPE_LOGOUT


class BaseTestCaseWithData(BaseTestCase):

    """ Add data... """

    def setUp(self):
        db.create_all()
        self.create_log_types()
        self.create_user_agents()
        self.create_sample_data()

    def create_log_types(self):
        log_login = LogTypeEntity.create(type=LOG_TYPE_LOGIN, description='')
        log_logout = LogTypeEntity.create(type=LOG_TYPE_LOGOUT, description='')
        self.assertEquals(1, log_login.id)
        self.assertEquals(2, log_logout.id)

    def create_user_agents(self):
        user_agent_string = ""
        hash = utils.compute_text_md5(user_agent_string)
        user_agent = UserAgentEntity.create(user_agent=user_agent_string,
                                            hash=hash,
                                            platform="Linux",
                                            browser="Firefox",
                                            version="latest",
                                            language="EN-US")
        self.assertIsNotNone(user_agent)

    def create_sample_data(self):
        """ Add some data """
        # == Create users
        added_date = datetime.today()
        access_end_date = utils.get_expiration_date(180)
        user = UserEntity.create(email="admin@example.com",
                                 first="First",
                                 last="Last",
                                 minitial="M",
                                 added_at=added_date,
                                 modified_at=added_date,
                                 email_confirmed_at=added_date,
                                 access_expires_at=access_end_date)

        # == Create roles
        role_admin = RoleEntity.create(name=ROLE_ADMIN, description='role')
        role_tech = RoleEntity.create(name=ROLE_TECHNICIAN, description='role')
