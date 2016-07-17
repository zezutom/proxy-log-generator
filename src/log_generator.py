#! /usr/bin/python
import logging
from optparse import OptionParser
from datetime import timedelta, datetime
import random
from random import randrange


def generate_event(timestamp):
    logging.info('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (timestamp,
                                           rand_ip(),
                                           rand_user_agent(),
                                           rand_auth(),
                                           rand_url(),
                                           rand_http_status(),
                                           rand_res_size()))


def generate_log(options):
    logging.basicConfig(filename=options.logfile, format='%(message)s', level=logging.DEBUG)
    current_time = datetime.now()
    timestamp = current_time - timedelta(hours=options.duration)
    while current_time > timestamp:
        generate_event(timestamp)
        timestamp = timestamp + timedelta(minutes=options.increment)


def read_options():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='logfile', help='Path to a log file. Default=logfile.log', default='logfile.log', type='string')
    parser.add_option('-t', '--time', dest='duration', help='Generate logs for X Hours. Default=48H ( 2 days)', default='48', type='int')
    parser.add_option('-i', '--increment', dest='increment', help='Generate logs every X minutes. Default=5min', default='5', type='int')
    (options, args) = parser.parse_args()
    return options


def rand_ip():
    invalid = [10, 127, 169, 172, 192]
    first = rand_octet()
    while first in invalid:
        first = rand_octet()
    return '.'.join([first, rand_octet(), rand_octet(), rand_octet()])


def rand_octet():
    return str(randrange(1, 256))


def rand_user_agent():
    user_agents = read_conf('user_agents.txt')
    return rand_item(user_agents)


# TODO not all requests are necessarily authenticated
def rand_auth():
    fnames = read_conf('fnames.txt')
    lnames = read_conf('lnames.txt')
    return ('.'.join([rand_item(fnames), rand_item(lnames)])).lower()


def read_conf(filename):
    return open('conf/%s'%filename, 'r').readlines()


def rand_bool():
    return bool(random.getrandbits(1))


# TODO add random resource links (images, html pages etc.)
def rand_url():
    first = ':'.join(['https' if rand_bool() else 'http', '//www'])
    fname = rand_item(read_conf('fnames.txt'))
    lname = rand_item(read_conf('lnames.txt'))
    delimiter = '-' if rand_bool() else ''
    return '.'.join([first, ('%s%s%s' % (fname, delimiter, lname)).lower(), 'com'])


def rand_http_status():
    return rand_item((200, 302, 404, 500))


# up until 5MB
def rand_res_size():
    return random.randrange(1, 5000000)

def rand_item(list):
    return str(list[randrange(0, len(list) - 1)]).strip()


def main():
    generate_log(options=read_options())

if __name__ == '__main__':
    main()
