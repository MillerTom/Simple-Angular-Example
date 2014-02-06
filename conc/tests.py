import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_jinja2')
        self.config.add_jinja2_search_path("conc:templates")

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .views import home
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info['project'], 'Celery on CentOS')
