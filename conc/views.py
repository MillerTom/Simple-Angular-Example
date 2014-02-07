from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from .tasks import get_repos, get_user_info
import time


@view_config(route_name='get_repos', renderer='home.jinja2')
def home(request):
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
        return {'project': 'Celery on CentOS'}


@view_config(route_name='get_user_info', renderer='json')
def user_info(request):
    """
    Similar to home view first checks the request and runs the celery task.
    """
    if request.method == 'POST':
        username = request.json_body['username']
        req = get_user_info.delay(username)
        info = req.get()
        return info