#! /usr/bin/python
import logging
from optparse import OptionParser
from datetime import timedelta, datetime
import random
from random import randrange


def generate_event(timestamp):
    logging.info('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (timestamp.strftime('%Y-%m-%d %H:%M:%S'),
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
        timestamp += timedelta(minutes=options.increment, seconds=randrange(0, 59))


def read_options():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='logfile', help='Path to a log file. Default=logfile.log',
                      default='logfile.log', type='string')
    parser.add_option('-t', '--time', dest='duration', help='Generate logs for X Hours. Default=48H ( 2 days)',
                      default='48', type='int')
    parser.add_option('-i', '--increment', dest='increment', help='Generate logs every X minutes. Default=5min',
                      default='5', type='int')
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


def rand_auth():
    if not rand_bool():
        return '-'
    fnames = read_conf('fnames.txt')
    lnames = read_conf('lnames.txt')
    return ('.'.join([rand_item(fnames), rand_item(lnames)])).lower()


def read_conf(filename):
    return open('conf/%s' % filename, 'r').readlines()


def rand_bool():
    return bool(random.getrandbits(1))


def rand_url():
    first = ':'.join(['https' if rand_bool() else 'http', '//www'])
    fname = rand_item(read_conf('fnames.txt'))
    lname = rand_item(read_conf('lnames.txt'))
    delimiter = '-' if rand_bool() else ''
    base_url = '.'.join([first, ('%s%s%s' % (fname, delimiter, lname)).lower(), 'com'])
    return ''.join([base_url, rand_resource()])


def rand_resource():
    depth = randrange(1, 5)
    suffixes = ['jpg', 'png', 'html', 'xml', 'php', 'asp']
    resource = ''
    for i in range(depth):
        resource = '/'.join([resource, str(randrange(1, 999))])
    return '.'.join([resource, rand_item(suffixes)])


def rand_http_status():
    return rand_item((200, 302, 404, 500))


# up until 5MB
def rand_res_size():
    return randrange(1, 5000000)


def rand_item(custom_list):
    return str(custom_list[randrange(0, len(custom_list) - 1)]).strip()


def main():
    generate_log(options=read_options())


if __name__ == '__main__':
    main()
