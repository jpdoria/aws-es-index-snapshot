# About

Register snapshot directory and take and restore snapshots of Elasticsearch Service indices.

# Dependencies

## Registration, Backup, and Restore
- S3 bucket
- IAM role

**Trust Relationship**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "es.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
} 
```

- IAM policy

**Permissions**

```json
 {
    "Version":"2012-10-17",
    "Statement":[
        {
            "Action":[
                "s3:ListBucket"
            ],
            "Effect":"Allow",
            "Resource":[
                "arn:aws:s3:::{name-of-the-newly-created-s3-bucket}"
            ]
        },
        {
            "Action":[
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "iam:PassRole"
            ],
            "Effect":"Allow",
            "Resource":[
                "arn:aws:s3:::{name-of-the-newly-created-s3-bucket}/*"
            ]
        }
    ]
} 
```

### Registering a Snapshot directory

Please follow the instructions how to register your snapshot directory with Amazon Elasticsearch Service [here](http://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-managedomains.html#es-managedomains-snapshot-registerdirectory).

Alternatively, you can run `aws_eis register` to register.

#### Example of registration using `aws-es-index-snapshot.py`

```
aws_eis register -r ap-southeast-1 -b my-es-snapshots -i es-iam-role -e search-myesdomain-xxxxxxxxxxxxxxxxxxxxxxxxxx.ap-southeast-1.es.amazonaws.com
```

## Local Machine

- [Python 3.6](https://www.python.org/downloads/)
- [Pip](https://pypi.python.org/pypi/pip)

## AWS Lambda
- IAM role using `AWSLambdaVPCAccessExecutionRole` policy
- Add Lambda's NAT IP to Elasticsearch Service Access Policy

# aws_eis

## Local Machine Setup

`pip install aws_eis`

## Usage

```
# aws_eis
usage: aws_eis [-h] {create,restore,cleanup,register,version} ...

Amazon ES Manual Index Snapshot

positional arguments:
  {create,restore,cleanup,register,version}
                        Available commands for this script.
    create              Create a snapshot of Elasticsearch indices
    restore             Restore a snapshot of Elasticsearch indices
    cleanup             Remove indices older than X day(s)
    register            Create S3 bucket, IAM role, IAM policy then register
                        the snapshot directory
    version             Display app version

optional arguments:
  -h, --help            show this help message and exit
#
```

# aws-es-index-snapshot-lambda.py

## AWS Lambda Setup
1. AWS Management Console > Lambda
1. Create a Lambda function > Blank function
1. Skip Configure triggers by clicking Next button
1. Give your function a name and a description
1. Choose Python 2.7 as Runtime
1. Code entry type: Upload a .ZIP file, then click Upload
1. Clone or download the code as zip
1. Change directory to `aws-es-index-snapshot/aws-es-index-snapshot-lambda`
1. Upload the `aws-es-index-snapshot-lambda.zip`
1. Create two environment variables for your Elasticsearch Service domain and retention period (days)
    - Key: ES_ENDPOINT | Value: search-myesdomain-xxxxxxxxxxxxxxxxxxxxxxxxxx.ap-southeast-1.es.amazonaws.com
    - Key: RET_PERIOD | Value: 30
1. Handler: aws-es-index-snapshot-lambda.lambda_handler
1. Role: Choose an existing role, then find the role you created
1. Memory: 128 MB and Timeout: 5 mins
1. VPC: Select your existing VPC
1. Subnets: Select your private subnets with NAT Gateway (2 subnets are required)
1. Security Groups: Select your security group that is allowed to have outbound connections (HTTP/HTTPS). Inbound rules are not required.
1. Click Next > Create function

## CloudWatch Events Setup

1. AWS Management Console > CloudWatch
1. Events > Rules > Create a new rule
1. Event selector: Schedule, fixed rate of 1 Day
1. Target: Lambda function, then select your aws-es-index-snapshot-lambda function
1. Click Configure details
1. Give your rule a name and a description
1. State should be Enabled
1. Click Create rule button

## Sample logs from CloudWatch Logs

```
START RequestId: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx Version: $LATEST
Getting indices older than 30 day(s)...
Skipping index: cwl-2017.01.19...
Skipping index: cwl-2017.01.17...
Skipping index: cwl-2017.01.30...
Skipping index: cwl-2017.02.03...
Skipping index: cwl-2017.02.06...
Skipping index: cwl-2017.01.16...
Skipping index: cwl-2017.02.07...
Creating snapshot...
SnapshotName: 20170208-042037
END RequestId: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
REPORT RequestId: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx	Duration: 1374.01 ms	Billed Duration: 1400 ms Memory Size: 128 MB	Max Memory Used: 12 MB
```

# Contributing

This project is still young and there are things that need to be done. If you have ideas that would improve this, feel free to contribute!

# License

MIT License

Copyright (c) 2017 John Paul P. Doria

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# References
https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-managedomains.html
https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html
