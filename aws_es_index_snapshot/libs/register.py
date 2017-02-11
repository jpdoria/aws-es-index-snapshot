from boto.connection import AWSAuthConnection
from libs.aws import Aws


class ESConnection(AWSAuthConnection):
    def __init__(self, region, **kwargs):
        super(ESConnection, self).__init__(**kwargs)
        self._set_auth_region_name(region)
        self._set_auth_service_name("es")

    def _required_auth_capability(self):
        return ['hmac-v4']


def register(args):
    aws = Aws()
    region = args.region
    bucket_name = args.bucket
    role_name = args.iam_role
    endpoint = args.endpoint
    client = ESConnection(
        region=region,
        host=endpoint
    )
    role_arn = aws.iam_create_role(bucket_name, role_name)

    aws.s3_create_bucket(region, bucket_name)
    print('Registering snapshot directory...')

    http_method = 'POST'
    snapshot_path = '/_snapshot/weblogs-index-backups'
    repository = {
        'type': 's3',
        'settings': {
            'bucket': bucket_name,
            'region': region,
            'role_arn': role_arn
        }
    }

    mr_resp = client.make_request(
        method=http_method,
        path=snapshot_path,
        data=json.dumps(repository)
    )

    print('Registered snapshot directory!')
