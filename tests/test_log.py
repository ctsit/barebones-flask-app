"""
Goal: test CRUD operations for LogType, Log, WebSession, UserAgent tables
"""
from datetime import datetime

from app.utils import compute_text_md5
from app.models.log_type_entity import LOG_TYPE_LOGIN, LOG_TYPE_LOGOUT
from app.models.log_type_entity import LogTypeEntity
from app.models.log_entity import LogEntity
from app.models.web_session_entity import WebSessionEntity
from app.models.user_agent_entity import UserAgentEntity

from .base_test import BaseTestCase


class TestLog(BaseTestCase):

    def test_log_creation(self):
        """ Test CRUD operations """

        # LogType
        log_login = LogTypeEntity.create(type=LOG_TYPE_LOGIN, description='')
        log_logout = LogTypeEntity.create(type=LOG_TYPE_LOGOUT, description='')
        self.assertEquals(1, log_login.id)
        self.assertEquals(2, log_logout.id)

        # UserAgent
        user_agent_string = "Long text..."
        hash = compute_text_md5(user_agent_string)
        user_agent = UserAgentEntity.create(user_agent=user_agent_string,
                                            hash=hash,
                                            platform="Linux",
                                            browser="Firefox",
                                            version="latest",
                                            language="EN-US")
        # print(user_agent)
        self.assertEquals(1, user_agent.id)
        self.assertEquals("467ffa17419afeffe09bb98af4828a30", user_agent.hash)
        self.assertEquals("Linux", user_agent.platform)
        self.assertEquals("latest", user_agent.version)
        self.assertEquals("EN-US", user_agent.language)

        # WebSession
        web_session = WebSessionEntity.create(user_agent_id=user_agent.id)
        self.assertEquals(1, web_session.id)
        self.assertEquals(user_agent, web_session.user_agent)
        # print(web_session.user_agent)

        # Log
        log = LogEntity.create(type_id=log_login.id,
                               web_session_id=web_session.id,
                               date_time=datetime.now(),
                               details='just a test')
        log2 = LogEntity.create(type_id=log_logout.id,
                                web_session_id=web_session.id,
                                date_time=datetime.now(),
                                details='just a test')

        self.assertEquals(1, log.id)
        self.assertEquals(2, log2.id)
        self.assertEquals(LOG_TYPE_LOGIN, log.log_type.type)
        self.assertEquals(LOG_TYPE_LOGOUT, log2.log_type.type)
        # print(log)
