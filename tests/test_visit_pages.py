"""
Goal: Simulate browsing of the pages in the url_map

Authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

from __future__ import print_function

from flask import url_for
from .base_test_with_data import BaseTestCaseWithData
from app.main import app

protected_pages = [
    '/loginExternalAuthReturn',
    '/admin',
    '/dashboard',
    '/logs',
    ]


class TestVisitPages(BaseTestCaseWithData):

    """ ha """

    def test_visit_pages(self):
        """ Verify that the pages without params render properly"""
        print("")

        for rule in app.url_map.iter_rules():
            if 'static' == rule.endpoint:
                continue

            url = url_for(rule.endpoint)

            # Calculate number of default-less parameters
            params = len(rule.arguments) if rule.arguments else 0
            params_with_default = len(rule.defaults) if rule.defaults else 0
            params_without_default = params - params_with_default

            # Skip routes with default-less parameters
            if params_without_default > 0:
                print("Skip parametrized page: {}".format(url))
                continue

            # Skip routes without a GET method
            if 'GET' not in rule.methods:
                print("Skip non-get page: {}".format(url))
                continue

            # Skip routes for protcted_pages
            if url in protected_pages:
                print("Skip special page: {}".format(url))
                continue

            # Simulate visiting the page
            print("Visiting page: {}".format(url))
            result = self.client.get(url, follow_redirects=True)
            print(result)

    def test_login(self):
        """ TODO: add user to database first """
        login_url = url_for('index')
        login_data = {'email': 'admin@example.com', 'password': 'password'}

        # @see "class EnvironBuilder"
        # https://github.com/mitsuhiko/werkzeug/blob/d4e8b3f46c51e7374388791282e66323f64b3068/werkzeug/test.py#L212
        wsgi_env = {
            'REMOTE_ADDR': '1.2.3.4',
            'HTTP_USER_AGENT':
            'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}

        with self.app.test_request_context(environ_base=wsgi_env):
            with app.test_client() as client:
                # Trigger execution of before_request()
                app.preprocess_request()
                response = client.post(login_url, login_data)
                print("Try to login response: {}".format(response))
                # self.assert_redirects(response, url_for('technician'))
