#!/usr/bin/env python

import pkg_resources
import sys
from aws_eis.lib import test_con, get_version
from aws_eis.lib import cleanup, create, register, restore, set_args


def main():
    parser = set_args()
    args = parser.parse_args()

    # Print help if no arguments are received
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Commands and their functions
    if args.command == 'create':
        test_con(args.endpoint)
        create(args)
    elif args.command == 'restore':
        test_con(args.endpoint)
        restore(args)
    elif args.command == 'cleanup':
        test_con(args.endpoint)
        cleanup(args)
    elif args.command == 'register':
        test_con(args.endpoint)
        register(args)
    elif args.command == 'version':
        print(pkg_resources.require('aws_eis')[0].version)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(1)
