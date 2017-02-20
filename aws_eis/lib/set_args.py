import argparse


def set_args():
    parser = argparse.ArgumentParser(
        description='Amazon ES Manual Index Snapshot',
    )
    subparsers = parser.add_subparsers(
        help='Available commands for this script.',
        dest='command'
    )

    """
    Create a snapshot
    Link to AWS Documentation: https://goo.gl/Pnkxl2
    """
    create = subparsers.add_parser(
        'create',
        help='Create a snapshot of Elasticsearch indices'
    )

    create.add_argument(
        '-e',
        '--endpoint',
        help="""Elasticsearch Service endpoint (e.g.,
             search-<domain>-<random string>.<region>.es.amazonaws.com)""",
        required=True
    )

    """
    Restore a snapshot
    Link to AWS Documentation: https://goo.gl/BH1MES
    """
    restore = subparsers.add_parser(
        'restore',
        help='Restore a snapshot of Elasticsearch indices'
    )

    restore.add_argument(
        '-e',
        '--endpoint',
        help="""Elasticsearch Service endpoint (e.g.,
             search-<domain>-<random string>.<region>.es.amazonaws.com)""",
        required=True
    )
    restore.add_argument(
        '-s',
        '--snapshot-name',
        help="""The name of snapshot you want to restore to
             Amazon Elasticsearch Service domain.""",
        required=True
    )

    """
    Clean up - remove indices older than X day(s)
    """
    cleanup = subparsers.add_parser(
        'cleanup',
        help='Remove indices older than X day(s)'
    )

    cleanup.add_argument(
        '-e',
        '--endpoint',
        help="""Elasticsearch Service endpoint (e.g.,
             search-<domain>-<random string>.<region>.es.amazonaws.com)""",
        required=True
    )
    cleanup.add_argument(
        '-r',
        '--retention-period',
        help='Snapshot retention period (days)',
        required=True
    )

    """
    Register a snapshot directory
    Link to AWS Documentation: https://goo.gl/QEQxJV
    """
    register = subparsers.add_parser(
        'register',
        help='Create S3 bucket, IAM role, IAM policy then register the \
              snapshot directory'
    )

    register.add_argument(
        '-b',
        '--bucket',
        help='Stores manual snapshots for your Amazon ES domain.',
        required=True
    )
    register.add_argument(
        '-e',
        '--endpoint',
        help="""Elasticsearch Service endpoint (e.g.,
             search-<domain>-<random string>.<region>.es.amazonaws.com)""",
        required=True
    )
    register.add_argument(
        '-i',
        '--iam-role',
        help="""Delegates permissions to Amazon Elasticsearch Service.
            The trust relationship for the role must specify Amazon
            Elasticsearch Service in the Principal statement. The role type
            must be Amazon EC2. The IAM role is also required to register
            your snapshot repository with Amazon ES. Only IAM users with
            access to this role may register the snapshot repository.""",
        required=True
    )
    register.add_argument(
        '-r', '--region',
        help='AWS region is a geographical area (e.g., ap-southeast-1)',
        required=True
    )

    """
    Check endpoint status
    """
    status = subparsers.add_parser(
        'status',
        help='Check endpoint status'
    )

    status.add_argument(
        '-e',
        '--endpoint',
        help="""Elasticsearch Service endpoint (e.g.,
             search-<domain>-<random string>.<region>.es.amazonaws.com)""",
        required=True
    )

    """
    Display app version
    """
    version = subparsers.add_parser(
        'version',
        help='Display app version'
    )

    return parser
