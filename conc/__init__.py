from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig('1L#^hgYrTa%snH&hjhfrk^JHEuK$bD&6waSJb^%hGFaSy')
    config = Configurator(settings=settings, session_factory=my_session_factory)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("conc:templates")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('get_repos', '/')
    config.add_route('get_user_info', '/user')
    config.scan()
    return config.make_wsgi_app()
