import unittest
import json

from pyramid import testing
from conc.views import home, user_info


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_jinja2')
        self.config.add_jinja2_search_path("conc:templates")

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info['project'], 'Celery on CentOS')

    def test_user_info(self):
        request = testing.DummyRequest()
        request.method = 'POST'
        request.json_body = {'username': 'millertom'}
        user = user_info(request)
        self.assertEqual(user['login'], 'millertom')
        self.assertEqual(user['followers'], 0)

    def test_task_get_repos(self):
        from conc.tasks import get_repos
        username = 'millertom'
        repos = get_repos(username)
        self.assertEqual(len(repos), 3)
        self.assertEqual(type(repos), type({}))

    def test_task_get_user_info(self):
        from conc.tasks import get_user_info
        username = 'millertom'
        user = get_user_info(username)
        self.assertEqual(user['login'], 'millertom')

    def test_task_get_repos_negative(self):
        from conc.tasks import get_repos
        username = ''
        repos = get_repos(username)
        self.assertEqual(repos[0], 'Not Found')
