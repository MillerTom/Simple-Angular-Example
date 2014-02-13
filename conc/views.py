from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from .tasks import (get_repos, get_user_info, user_auth,
                    get_user, get_emails, get_notifications,
                    get_starred_repos, client_id)
import requests
import json


@view_config(route_name='home', renderer='home.jinja2')
def home(request):
    session = request.session
    return {'project': 'Celery on CentOS',
            'client_id': client_id,
            'session': session}


@view_config(route_name='get_repos')
def get_user_repos(request):
    """
    Checks the request method and renders the template if it's GET
    If request method is POST it runs the celery task and returns the result as json
    """
    if request.method == 'POST':
        username = request.json_body['username']
        repos = get_repos.delay(username)
        r_list = repos.get()
        return render_to_response('json', r_list, request=request)
    else:
        return render_to_response('repos.jinja2', {'project': 'Celery on CentOS'}, request=request)


@view_config(route_name='get_user_info', renderer='json')
def user_info(request):
    """
    Similar to home view, first checks the request and runs the celery task.
    """
    if request.method == 'POST':
        username = request.json_body['username']
        req = get_user_info.delay(username)
        info = req.get()
        return info


@view_config(route_name='login')
def git_login(request):
    """
    Makes a request to GitHub Oauth authorization to get access token.
    """
    session_code = request.params['code']
    login = user_auth.delay(session_code)
    access_token = login.get()
    session = request.session
    session['access_token'] = access_token
    return HTTPFound('/profile')


@view_config(route_name='profile', renderer='profile.jinja2')
def profile(request):
    session = request.session
    try:
        token = session['access_token']
    except KeyError:
        return HTTPFound('/')
    if request.method == 'POST':
        result = get_user.delay(token)
        emails = get_emails.delay(token)
        notifications = get_notifications.delay(token)
        starred_repos = get_starred_repos.delay(token)

        res = result.get()
        mails = emails.get()
        notifs = notifications.get()
        starred = starred_repos.get()

        res['mails'] = mails
        res['notifs'] = notifs
        res['starred'] = starred
        return render_to_response('json', res, request=request)
    else:
        return {'project': 'Celery on CentOS'}


@view_config(route_name='logout')
def logout(request):
    session = request.session
    session.clear()
    return HTTPFound('/')