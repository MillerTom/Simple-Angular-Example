from pyramid.view import view_config
from pyramid.renderers import render_to_response
from .tasks import get_repos, get_user_info, search_users
import time


@view_config(route_name='get_repos', renderer='home.jinja2')
def home(request):
    if request.method == 'POST':
        username = request.json_body['username']
        #time.sleep(2)
        repos = get_repos.delay(username)
        #time.sleep(3)
        r_list = repos.get()
        return render_to_response('json', r_list, request=request)
    else:
        return {'project': 'Celery on CentOS'}


@view_config(route_name='get_user_info')
def user_info(request):
    if request.method == 'POST':
        username = request.json_body['username']
        #time.sleep(2)
        req = get_user_info.delay(username)
        #time.sleep(3)
        info = req.get()
        return render_to_response('json', info, request=request)


@view_config(route_name='search_users')
def search(request):
    if request.method == 'POST':
        username = request.json_body['username']
        req = search_users.delay(username)
        time.sleep(2)
        results = req.get()
        return render_to_response('json', results, request=request)