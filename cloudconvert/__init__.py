from cloudconvert.cloudconvertrestclient import *
from cloudconvert.task import Task
from cloudconvert.job import Job
from cloudconvert.webhook import Webhook

API_KEY = ''
sandbox = True


def configure():
    """
    Configure the REST Client With Latest API Key and Mode
    :return:
    """
    set_config(token=API_KEY, sandbox=sandbox)


def default():
    """
    Configure the REST Client With Default API Key and Mode
    :return:
    """
    default_client()

