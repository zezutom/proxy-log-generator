#! /usr/bin/python
import logging
import random
import os
import re
import time
import json
import requests
from requests import ConnectionError
from argparse import ArgumentParser
from datetime import timedelta, datetime
from random import randrange


def configure_logging(logfile):
    # Enable fine grained logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Log message format (don't print the level as it is all the same for each of the handlers)
    formatter = logging.Formatter("%(message)s")

    # Console logs: info level
    add_log_handler(logger, logging.StreamHandler(), logging.INFO, formatter)

    # Error logs
    add_log_handler(logger, logging.FileHandler("error.log"), logging.ERROR, formatter)

    # Application log: debug level
    add_log_handler(logger, logging.FileHandler(logfile), logging.DEBUG, formatter)


def add_log_handler(logger, handler, level, formatter):
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def generate_event(timestamp, args=None):
    # Sanity check
    if hasattr(args, 'url') and args.url:
        return post_event(timestamp, args)

    # Generate a random event
    event = {
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'ip': rand_ip(),
        'user_agent': rand_user_agent(),
        'authenticated': rand_auth(rand_bool()),
        'url': rand_url(),
        'res_status': rand_http_status(),
        'res_size': rand_res_size()
    }

    # log it
    logging.debug('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}'.format(event['timestamp'],
                                                             event['ip'],
                                                             event['user_agent'],
                                                             event['authenticated'],
                                                             event['url'],
                                                             event['res_status'],
                                                             event['res_size']))
    return event


def generate_events(timestamp, volume):
    random_volume = randrange(1, volume)
    i = 0
    while i < random_volume:
        generate_event(timestamp)
        i += 1


def generate_log(args):
    configure_logging(args.file)
    current_time = datetime.now()
    timestamp = current_time - parse_duration(args)

    # DDoS?
    if args.ddos:
        (volume, start, duration) = parse_ddos_conf(args)
        ddos_timestamp = timestamp + start
        current_time = start + duration

        logging.info('Enabling DDOS: volume = %s | start = %s | duration = %s' % (volume, start, duration))

        # Create a peak in traffic volume
        while current_time > start:
            generate_events(ddos_timestamp, volume)
            ddos_timestamp += parse_increment(args)

        # Generate a normal load for the remaining time slot, if any
        generate_events(ddos_timestamp, timestamp)
    else:
        # Generate a normal load
        logging.info('Creating a normal load: from %s to %s' %
                     (timestamp_to_string(timestamp),
                      timestamp_to_string(current_time)))
        generate_events(current_time, timestamp)


def timestamp_to_string(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def parse_ddos_conf(options):
    match = re.match(r'(\d+) (\d+)(h|m|s) (\d+)(h|m|s)', options.ddos_conf, re.IGNORECASE)
    if match:
        volume = int(match.group(1))

        start = int(match.group(2))
        start_time = {
            'h': timedelta(hours=start),
            'm': timedelta(minutes=start),
            's': timedelta(seconds=start)
        }[match.group(3).lower()]

        duration = int(match.group(4))
        duration_time = {
            'h': timedelta(hours=duration),
            'm': timedelta(minutes=duration),
            's': timedelta(seconds=duration)
        }[match.group(5).lower()]
        return volume, start_time, duration_time
    else:
        logging.error('Invalid duration: \'%s\' using default '
                      '(1000 concurrent connections, starts in 4 hours, takes 10 minutes)' % options.ddos_conf)
        return 10000, timedelta(hours=4), timedelta(minutes=10)


def parse_duration(options):
    match = re.match(r'(\d+)(d|h|m|s)', options.time, re.IGNORECASE)
    if match:
        duration = int(match.group(1))
        return {
            'd': timedelta(days=duration),
            'h': timedelta(hours=duration),
            'm': timedelta(minutes=duration),
            's': timedelta(seconds=duration)
        }[match.group(2).lower()]
    else:
        logging.error('Invalid duration: \'%s\' using default (2 days)' % options.time)
        return timedelta(days=2)


def parse_increment(options):
    match = re.match(r'(\d+)(ms|m|s)', options.increment, re.IGNORECASE)
    if match:
        increment = int(match.group(1))
        return {
            'm': timedelta(minutes=increment, seconds=randrange(0, 59)),
            's': timedelta(seconds=increment, milliseconds=randrange(0, 1000)),
            'ms': timedelta(milliseconds=increment, microseconds=randrange(0, 1000))
        }[match.group(2).lower()]
    else:
        logging.error('Invalid increment: \'%s\' using default (5 minutes)' % options.increment)
        return timedelta(minutes=5, seconds=randrange(0, 59))


def read_args():
    parser = ArgumentParser(description='Process user input')
    parser.add_argument('-s', '--stream', help='Stream inbound events at ms frequency. Default=200ms', type=int,
                        default=200)
    parser.add_argument('-u', '--url', help='URL of a remote endpoint the generated events are streamed to.')
    parser.add_argument('-f', '--file', help='Path to a log file. Default=logfile.log', default='logfile.log')
    parser.add_argument('-t', '--time', help='Generate logs for X days (d), hours (h), '
                                             'minutes (m) or seconds (s). Default=1d (1 day)', default='1d')
    parser.add_argument('-i', '--increment', help='Generate logs every X minutes (m), seconds (s) '
                                                  'or milliseconds (ms). Default=5m (5 minutes)', default='5m')
    parser.add_argument('-v', '--volume', help='How many concurrent connections are considered'
                                               ' a legitimate usual load. Default=100',
                        type=int, default=100)
    parser.add_argument('-d', '--ddos', help='Trigger a DDoS attack? Default=false',
                        action='store_true', default=False)
    parser.add_argument('-c', '--ddos_conf', help='Defines a DDoS attack in terms of severity, timing '
                                                  'and duration. By default, a DDoS is defined '
                                                  'as \'1000 4h 10m\'. This means that a 10x more '
                                                  'events than the usual load (see -v) are generated '
                                                  'after 4 hours into the day and the attack is '
                                                  'carried for 10 minutes. Feel free to override '
                                                  'this definition. Supported time units are hours(h), '
                                                  'minutes (m) and seconds (s).', default='1000 4h 10m')

    args = parser.parse_args()
    return args


def rand_ip():
    invalid = map(lambda x: str(x), (10, 127, 169, 172, 192))
    first = rand_octet()
    while first in invalid:
        first = rand_octet()
    return '.'.join([first, rand_octet(), rand_octet(), rand_octet()])


def rand_octet():
    return str(randrange(1, 256))


def rand_user_agent():
    user_agents = read_conf('user_agents.txt')
    return rand_item(user_agents)


def rand_auth(anonymous):
    if anonymous:
        return '-'
    fnames = read_conf('fnames.txt')
    lnames = read_conf('lnames.txt')
    return ('.'.join([rand_item(fnames), rand_item(lnames)])).lower()


def read_conf(filename):
    src_dir = os.path.dirname(os.path.abspath(__file__))
    return open('%s/conf/%s' % ('%s/..' % src_dir, filename), 'r').readlines()


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


def post_event(timestamp, args):
    event = generate_event(timestamp)
    json_str = json.dumps(event)
    logging.debug(json_str)
    return requests.post(args.url, json=json_str)


def send_event(event_handler, *args):
    event_handler(*args)


def main():
    args = read_args()
    if not args.stream:
        generate_log(args=read_args())
        return

    # Enable fine grained logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Log message format (don't print the level as it is all the same for each of the handlers)
    formatter = logging.Formatter("%(message)s")

    # Console logs: info level
    add_log_handler(logger, logging.StreamHandler(), logging.DEBUG, formatter)

    # Resolve event delay
    delay = args.stream / 1000.0

    # Resolve event handler
    event_handler = post_event if args.url else generate_event

    # Generate events
    err_count = 0
    while True:
        try:
            send_event(event_handler, datetime.now(), args)
            time.sleep(delay)
        except KeyboardInterrupt:
            print 'Terminating..'
            break
        except ConnectionError:
            err_count += 1
            if err_count >= 3:
                print 'The remote service is inaccessible, terminating ..'
                break
            else:
                print 'Cannot connect to the remote service. Retry started ..'
                # Provide increasingly more time for the connection to recover
                time.sleep(delay * err_count)


if __name__ == '__main__':
    main()
