import json
import random
import re
import string
from datetime import datetime

import cherrypy
import yaml

__author__ = 'jason'


def handle_json(headers):
    rawbody = cherrypy.request.body.read(int(headers))
    return json.loads(rawbody)


def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_config(config_file):
    try:
        config_handle = open(config_file)
        config_string = config_handle.read()
        config_dict = yaml.load(config_string)
    except Exception, e:
        raise Exception('parse_config failed on ' + config_file + ': ' + str(e))
    return config_dict


def get_datetime_random_string(length):
    date_string = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    random_string = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(length))
    return '-' + date_string + '-' + random_string


def get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(length))


def get_username(env):
    if env.get('SSL_CLIENT_S_DN') is None:
        return None
    username = env['SSL_CLIENT_S_DN']
    if re.match('-ds$', username) is None:
        return None
    return username.replace('-ds', '')

