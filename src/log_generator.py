#! /usr/bin/python
import logging
import random
import os
import re
from optparse import OptionParser
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


def generate_event(timestamp, volume):
    random_volume = randrange(1, volume)
    i = 0
    while i < random_volume:
        logging.debug('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                      rand_ip(),
                                                      rand_user_agent(),
                                                      rand_auth(rand_bool()),
                                                      rand_url(),
                                                      rand_http_status(),
                                                      rand_res_size()))
        i += 1


def generate_log(options):
    configure_logging(options.logfile)
    current_time = datetime.now()
    timestamp = current_time - parse_duration(options)

    # DDoS?
    if options.ddos:
        (volume, start, duration) = parse_ddos_conf(options)
        ddos_timestamp = timestamp + start
        current_time = start + duration

        logging.info('Enabling DDOS: volume = %s | start = %s | duration = %s' % (volume, start, duration))

        # Create a peak in traffic volume
        while current_time > start:
            generate_event(ddos_timestamp, volume)
            ddos_timestamp += parse_increment(options)

        # Generate a normal load for the remaining time slot, if any
        generate_events(ddos_timestamp, timestamp, options)
    else:
        # Generate a normal load
        logging.info('Creating a normal load: from %s to %s' %
                     (timestamp_to_string(timestamp),
                      timestamp_to_string(current_time)))
        generate_events(current_time, timestamp, options)


def timestamp_to_string(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def generate_events(current_time, timestamp, options):
    while current_time > timestamp:
        generate_event(timestamp, options.volume)
        timestamp += parse_increment(options)


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
    match = re.match(r'(\d+)(d|h|m|s)', options.duration, re.IGNORECASE)
    if match:
        duration = int(match.group(1))
        return {
            'd': timedelta(days=duration),
            'h': timedelta(hours=duration),
            'm': timedelta(minutes=duration),
            's': timedelta(seconds=duration)
        }[match.group(2).lower()]
    else:
        logging.error('Invalid duration: \'%s\' using default (2 days)' % options.duration)
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


def read_options():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='logfile', help='Path to a log file. Default=logfile.log',
                      default='logfile.log', type='string')
    parser.add_option('-t', '--time', dest='duration', help='Generate logs for X days (d), hours (h), '
                                                            'minutes (m) or seconds (s). Default=1d (1 day)',
                      default='1d', type='string')
    parser.add_option('-i', '--increment', dest='increment', help='Generate logs every X minutes (m), seconds (s) '
                                                                  'or milliseconds (ms). Default=5m (5 minutes)',
                      default='5m', type='string')
    parser.add_option('-v', '--volume', dest='volume', help='How many concurrent connections are considered'
                                                            ' a legitimate usual load. Default=100',
                      default=100, type='int')
    parser.add_option('-d', '--ddos', dest='ddos', help='Trigger a DDoS attack? Default=false',
                      choices=[True, False], default=False, type='choice')
    parser.add_option('-c', '--ddos-conf', dest='ddos_conf', help='Defines a DDoS attack in terms of severity, timing '
                                                                  'and duration. By default, a DDoS is defined '
                                                                  'as \'1000 4h 10m\'. This means that a 10x more '
                                                                  'events than the usual load (see -v) are generated '
                                                                  'after 4 hours into the day and the attack is '
                                                                  'carried for 10 minutes. Feel free to override '
                                                                  'this definition. Supported time units are hours(h), '
                                                                  'minutes (m) and seconds (s).',
                      default='1000 4h 10m', type='string')

    (options, args) = parser.parse_args()
    return options


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


def main():
    generate_log(options=read_options())


if __name__ == '__main__':
    main()
