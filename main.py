import sys
import json
import argparse

import pystache

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filter', nargs='*', default=[],
                    help='[FIELD].[FIELD]=[VALUE] - field and value to filter log by')
parser.add_argument('--format', default='', help='file with pystache template')

template = '[{{@timestamp}}] {{@fields.level}} {{@message}}'  # default template
filter_separator = '.'  # default filter separator
filters = {
    '@fields.level': 'INFO'
}

args = parser.parse_args()
if args.filter:
    filters = dict((k.strip(), v.strip()) for k, v in (item.split('=') for item in args.filter))

if args.format:
    try:
        with open(args.format, 'r') as f:
            for line in f:
                if len(line.strip()) > 0:
                    template = line
                    break
    except IOError:
        print('File \'' + args.format + '\' does not exist')
        exit(1)

'''
Filter array by given value in a given field. Path to a field separated by '.'
'''


def filter_string(string, k, v):
    keys = k.split(filter_separator)
    for k in keys:
        try:
            string = string[k]
        except KeyError:
            return False
    return string == v


'''
Main loop
'''

try:
    while True:
        line = sys.stdin.readline()
        data = json.loads(line)
        display = True
        for key, value in filters.items():
            if not filter_string(data, key, value):
                display = False

        if display:
            print(pystache.render(template, data))
except KeyboardInterrupt:
    print('bye')
    exit(0)
