#! /usr/bin/python
import ConfigParser
import os
import sys

# Project root directory
ROOT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../')

# Configuration directory
CONFIG_DIR = os.path.join(ROOT_DIR, 'conf')
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# Path to the app config file
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, 'app.ini')

# Config parser
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE_PATH)


def load_data(filename):
    return open(os.path.join(DATA_DIR, filename), 'r').readlines()


def read_conf(section, key, default_value=None, type=str):
    try:
        value = config.get(section, key)
        if value == -1:
            print 'No such key "{0}". Returning a default value "{1}"'.format(key, default_value)
            return default_value
        else:
            # todo type check - see 'type'
            return type(value)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print 'Error when parsing "{0}.{1}". Returning a default value "{2}"'.format(section, key, default_value)
        return default_value


def get_template_folder():
    return get_resource_dir('template_folder')


def get_static_folder():
    return get_resource_dir('static_folder')


def get_resource_dir(name):
    return os.path.join(ROOT_DIR, read_conf('App', name))