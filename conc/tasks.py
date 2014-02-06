from celery import Celery
from celery.task import task
import requests


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
    """
    Another simple task to retrieve user information from GitHub.
    """
    r = requests.get(
        'https://api.github.com/users/'+username+'?client_id='+client_id+'&client_secret='+client_secret
    )

    if r.ok:
        info = r.json()
        return info