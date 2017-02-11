import boto3


class Aws:
    def __init__(self):
        self.iam = boto3.client('iam')
        self.s3 = boto3.client('s3')

    def iam_create_role(self, bucket_name, role_name):
        print('Creating IAM role {}...'.format(role_name))

        assume_role_policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': '',
                    'Effect': 'Allow',
                    'Principal': {
                        'Service': 'es.amazonaws.com'
                    },
                    'Action': 'sts:AssumeRole'
                }
            ]
        }
        perm_policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': [
                        's3:ListBucket'
                    ],
                    'Effect':'Allow',
                    'Resource': [
                        'arn:aws:s3:::{}'.format(bucket_name)
                    ]
                },
                {
                    'Action': [
                        's3:GetObject',
                        's3:PutObject',
                        's3:DeleteObject',
                        'iam:PassRole'
                    ],
                    'Effect':'Allow',
                    'Resource': [
                        'arn:aws:s3:::{}/*'.format(bucket_name)
                    ]
                }
            ]
        }
        cr_resp = self.iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy)
        )
        role_arn = cr_resp['Role']['Arn']
        cp_resp = self.iam.create_policy(
            PolicyName=role_name,
            PolicyDocument=json.dumps(perm_policy),
            Description='Policy for aws-es-index-snapshot'
        )
        policy_arn = cp_resp['Policy']['Arn']

        self.iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print('RoleName: {}'.format(role_name))
        print('RoleArn: {}'.format(role_arn))
        print('PolicyArn: {}'.format(policy_arn))

        return role_arn

    def s3_create_bucket(self, region, bucket_name):
        print('Creating {0} bucket in S3 ({1})...'
              .format(bucket_name, region))

        response = self.s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
        bucket_loc = response['Location']
        bucket_arn = 'arn:aws:s3:::{}'.format(bucket_name)

        print('BucketName: {}'.format(bucket_name))
        print('Location: {}'.format(bucket_loc))
        print('BucketArn: {}'.format(bucket_arn))
