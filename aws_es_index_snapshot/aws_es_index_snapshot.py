#!/usr/bin/env python

import sys

from libs.checks import get_version, test_con
from libs.cleanup import cleanup
from libs.create import create
from libs.register import register
from libs.restore import restore
from libs.set_args import set_args


def main():
    parser = set_args()
    args = parser.parse_args()

    # Print help if no arguments are received
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Test connection
    boolean, msg, status_code = test_con(args.endpoint)
    es_version = get_version(args.endpoint)

    if boolean is True:
        print('ESVersion: {}'.format(es_version))
        print('Connection: OK')
        print('Status: {}\n'.format(status_code))
    else:
        print(json.loads(msg)['Message'])
        print('Status: {}'.format(status_code))
        sys.exit(1)

    # Commands and their functions
    if args.command == 'create':
        create(args)
    elif args.command == 'restore':
        restore(args)
    elif args.command == 'cleanup':
        cleanup(args)
    elif args.command == 'register':
        register(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(1)
