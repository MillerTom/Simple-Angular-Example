CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
BROKER_URL = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_IMPORTS = ('conc.tasks', )
CELERY_ANNOTATIONS = {'*': {'rate_limit': '10/s'}}