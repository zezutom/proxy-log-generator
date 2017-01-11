#! /usr/bin/python
import random
from datetime import datetime
from random import randrange

import app_util


# Generate a random event
def create_event(timestamp=datetime.now()):
    return {
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'ip': rand_ip(),
        'user_agent': rand_user_agent(),
        'authenticated': rand_auth(rand_bool()),
        'url': rand_url(),
        'res_status': rand_http_status(),
        'res_size': rand_res_size()
    }


def rand_ip():
    def rand_octet():
        return str(randrange(1, 256))
    invalid = map(lambda x: str(x), (10, 127, 169, 172, 192))
    first = rand_octet()
    while first in invalid:
        first = rand_octet()
    return '.'.join([first, rand_octet(), rand_octet(), rand_octet()])


def rand_url():
    first = ':'.join(['https' if rand_bool() else 'http', '//www'])
    fname = rand_item(app_util.load_data('fnames.txt'))
    lname = rand_item(app_util.load_data('lnames.txt'))
    delimiter = '-' if rand_bool() else ''
    base_url = '.'.join([first, ('%s%s%s' % (fname, delimiter, lname)).lower(), 'com'])
    return ''.join([base_url, rand_resource()])


def rand_http_status():
    return int(rand_item([200, 302, 404, 500, 502, 503]))


def rand_user_agent():
    user_agents = app_util.load_data('user_agents.txt')
    return rand_item(user_agents)


def rand_auth(anonymous=False):

    if anonymous:
        return '-'

    fnames = app_util.load_data('fnames.txt')
    lnames = app_util.load_data('lnames.txt')
    return ('.'.join([rand_item(fnames), rand_item(lnames)])).lower()


def rand_item(custom_list):
    item = custom_list[randrange(0, len(custom_list) - 1)]
    return item.replace('\n', '').replace('\r', '') if isinstance(item, basestring) else item


def rand_resource():
    depth = randrange(1, 5)
    suffixes = ['jpg', 'png', 'html', 'xml', 'php', 'asp']
    resource = ''
    for i in range(depth):
        resource = '/'.join([resource, str(randrange(1, 999))])
    return '.'.join([resource, rand_item(suffixes)])


# up until 5MB
def rand_res_size():
    return randrange(1, 5000000)


def rand_bool():
    return bool(random.getrandbits(1))

