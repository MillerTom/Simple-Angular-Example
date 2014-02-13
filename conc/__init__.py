from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig('1L#^hgYrTa%snH&hjhfrk^JHEuK$bD&6waSJb^%hGFaSy')
    authn_policy = AuthTktAuthenticationPolicy('4vT0fgYrTa$snf+JhGfPh*hRwGK%dF=gr4waSJbL*hGFaSy', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, session_factory=my_session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("conc:templates")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('get_repos', '/repos')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('profile', '/profile')
    config.add_route('get_user_info', '/user')
    config.scan()
    return config.make_wsgi_app()