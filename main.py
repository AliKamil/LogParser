import sys
import json
import argparse

import pystache

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filter', nargs='*', default='')

template = '[{{@timestamp}}] {{@fields.level}} {{@message}}'  # default template
filter_separator = '.'  # default filter separator
filters = {
    '@fields.level': 'INFO'
}

args = parser.parse_args()
if len(args.filter) >= 0:
    filters = dict((k.strip(), v.strip()) for k, v in (item.split('=') for item in args.filter))

'''
Filter array by given value in a given field. Path to a field separated by '.'
'''


def Filter(data, key, value):
    keys = key.split(filter_separator)
    for key in keys:
        try:
            data = data[key]
        except KeyError:
            return False
    return data == value


'''
Main loop
'''
try:
    while True:
        line = sys.stdin.readline()
        data = json.loads(line)
        display = True
        for key, value in filters.iteritems():
            if not Filter(data, key, value):
                display = False

        if display:
            print(pystache.render(template, data))
except KeyboardInterrupt:
    print('bye')
