# Gunicorn configuration file
from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


name = 'Project_name'
# bind = '0.0.0.0:8000'
max_requests = 1000
worker_class = 'gevent'
workers = max_workers()
reload = True
deamon = True
accesslog = '/log/gunicorn/gunicorn-access.log'
errorlog = '/log/gunicorn/gunicorn-error.log'
loglevel = 'info'
