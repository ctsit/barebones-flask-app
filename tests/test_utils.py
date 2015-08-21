'''
Goal: test functions in utils.py
'''

import os
import time
from app import utils
from .base_test import BaseTestCase


class UtilsTests(BaseTestCase):

    def test_create_salt(self):
        '''
        Verify the remote address reading
        https://realpython.com/blog/python/python-web-applications-with-flask-part-iii/
        '''
        # add testing request context
        # http://flask.pocoo.org/docs/0.10/api/#flask.ctx.RequestContext
        wsgi_env = {
            'REMOTE_ADDR': os.environ.get('REMOTE_ADDR', '1.2.3.4'),
            'HTTP_USER_AGENT': os.environ.get('HTTP_USER_AGENT', 'cURL')}

        # from werkzeug.datastructures import Headers
        # headers = Headers([('Referer', '/example/url')])
        # with app.test_request_context(environ_base=wsgi_env, headers=headers)

        with self.app.test_request_context(environ_base=wsgi_env):
            actual_ip = utils._get_remote_addr()
            actual_agent = utils._get_user_agent()
            actual_hash = utils._create_salt()

            self.assertEquals('1.2.3.4', actual_ip)
            self.assertEquals('cURL', actual_agent)
            self.assertEquals(16, len(actual_hash))

    def test_generate_sha512_hmac(self):
        expected = '8vhMgmofeNDCISwvPc9yB7XQiNSPZHwDVz6kuYuA7aPA43j8RQVy+xwI2+87u3Pkpvq/qiuRuDreUoSxblqGzA=='
        actual = utils._generate_sha512_hmac('pepper', 'salt', 'password')
        self.assertEquals(actual, expected)

    def test_generate_auth(self):
        wsgi_env = {
            'REMOTE_ADDR': os.environ.get('REMOTE_ADDR', '1.2.3.4'),
            'HTTP_USER_AGENT': os.environ.get('HTTP_USER_AGENT', 'cURL')}

        with self.app.test_request_context(environ_base=wsgi_env):
            salt, actual_pass = utils.generate_auth('pepper', 'password')
            self.assertIsNotNone(actual_pass)
            self.assertEquals(88, len(actual_pass))

    def test_clean_int(self):
        """
        Verify common cases
        """
        cases = [
            {"x": None,     "exp": None},
            {"x": "",       "exp": None},
            {"x": "  ",     "exp": None},
            {"x": "  0x0",  "exp": None},
            {"x": "-1",     "exp": None},
            {"x": "-0.3",   "exp": None},
            {"x": "0.0",    "exp": None},
            {"x": "0",      "exp": 0},
            {"x": "0.3",    "exp": None},
            {"x": "01",     "exp": 1},
            {"x": "2",      "exp": 2},
            {"x": 3,        "exp": 3},
            {"x": 1.2,      "exp": None},
            {"x": 123,      "exp": 123},
        ]

        for case in cases:
            actual = utils.clean_int(case['x'])
            expected = case['exp']
            self.assertEquals(actual, expected)

    def test_pack(self):
        self.assertEquals('{"message":"msg","status":"error"}',
                          utils.pack_error("msg")
                          .replace(' ', '').replace('\n', ''))

    def test_compute_text_md5(self):
        """ verify md5 generator """
        text = 'text'
        self.assertEquals('1cb251ec0d568de6a929b520c4aed8d1',
                          utils.compute_text_md5(text))

    def test_get_email_token(self):
        email = 'a@a.com'
        salt = 'salt'
        secret = 'secret'
        token = utils.get_email_token(email, salt, secret)
        self.assertEquals('ImFAYS5jb20i', token[0:12])
        decoded = utils.get_email_from_token(token, salt, secret)
        self.assertEquals(email, decoded)
        time.sleep(2)

        with self.assertRaises(Exception) as context:
            decoded = utils.get_email_from_token(token, salt,
                                                 secret, max_age=1)
        self.assertTrue('Signature age 2 > 1 seconds' in context.exception)

    def test_localize_datetime_none_value(self):
        self.assertEquals('', utils.localize_datetime(None))

    def test_localize_est_datetime_none_value(self):
        self.assertEquals('', utils.localize_est_datetime(None))
