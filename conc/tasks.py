from celery import Celery
from celery.task import task
import requests


app = Celery('tasks')
app.config_from_object('conc.celeryconfig')

# Github API Credentials
client_id = 'b2c60ec1b36121a410a2'
client_secret = 'd8f9d0a084ff950474f3830705e1f269cae249b7'

@task
def get_repos(username):

    r = requests.get(
        'https://api.github.com/users/'+username+'/repos?client_id='+client_id+'&client_secret='+client_secret
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
    r = requests.get(
        'https://api.github.com/users/'+username+'?client_id='+client_id+'&client_secret='+client_secret
    )

    if r.ok:
        info = r.json()
        return info


@task
def search_users(username):
    r = requests.get(
        'https://api.github.com/search/users?q='+username+'&sort=ASC'+'?client_id='+client_id+'&client_secret='+client_secret
    )

    if r.ok:
        u = r.json()
        users = u['items']
        return users