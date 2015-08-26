'''
Goal: test functions in routes/api.py
'''

from .base_test import BaseTestCase
from app.routes.api import check_email_config

class RoutesApiTests(BaseTestCase):

    def test_check_email_config(self):
        errors = [
            'Emailing param MAIL_USERNAME was not configured.',
            'Emailing param MAIL_PASSWORD was not configured.',
            'Emailing param MAIL_SERVER was not configured.',
            'Emailing param MAIL_PORT was not configured.']
        passed, actual_errors = check_email_config()
        self.assertFalse(passed)
        self.assertEquals(errors, actual_errors)
