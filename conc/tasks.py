from celery import Celery
from celery.task import task
import requests
import json


# Celery app and configuration.
app = Celery('tasks')
app.config_from_object('conc.celeryconfig')

# Github API Credentials
client_id = 'b2c60ec1b36121a410a2'
client_secret = 'd8f9d0a084ff950474f3830705e1f269cae249b7'


@task
def get_repos(username):
    """
    Simple celery task. Makes a request to GitHub API
    and retrieves the repository list for the given username.
    Packs them in a dictionary and returns it.
    """
    r = requests.get(
        'https://api.github.com/users/' + username + '/repos?client_id=' + client_id + '&client_secret=' + client_secret
    )

    if r.ok:
        req = r.json()
        repo_names = [i['name'] for i in req]
        repo_urls = [i['html_url'] for i in req]
        repos = dict(zip(repo_names, repo_urls))
    else:
        repos = [r.reason]
    return repos


@task
def get_user_info(username):
    """
    Another simple task to retrieve user information from GitHub.
    """
    r = requests.get(
        'https://api.github.com/users/' + username + '?client_id=' + client_id + '&client_secret=' + client_secret
    )

    if r.ok:
        info = r.json()
        return info


@task
def user_auth(code):
    """
    GitHub API User Authentication
    """
    url = 'https://github.com/login/oauth/access_token'
    session_code = code
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {'client_id': client_id,
            'client_secret': client_secret,
            'code': session_code}
    result = requests.post(url, data=json.dumps(data), headers=headers)
    access_token = json.loads(result.content)['access_token']
    scopes = json.loads(result.content)['scope'].split(',')
    if 'user' in scopes:
        return access_token


@task
def get_user(key):
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'token '+key}
    url = 'https://api.github.com/user'
    result = requests.get(url, headers=headers)
    return result.json()


@task
def get_emails(key):
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'token '+key}
    url = 'https://api.github.com/user/emails'
    result = requests.get(url, headers=headers)
    return result.json()


@task
def get_notifications(key):
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'token '+key}
    url = 'https://api.github.com/notifications'
    result = requests.get(url, headers=headers)
    return result.json()


@task
def get_starred_repos(key):
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'token '+key}
    url = 'https://api.github.com/user/starred'
    result = requests.get(url, headers=headers)
    return result.json()