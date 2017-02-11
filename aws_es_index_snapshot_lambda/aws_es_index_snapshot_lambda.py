# AWS Documentation: https://goo.gl/0wpSJm

import json
import os
import re
import time
import requests
from datetime import datetime

dt_now = datetime.utcnow().strftime('%Y%m%d-%H%M%S')


def create_snapshot(endpoint):
    print('Creating snapshot...')
    requests.put('https://{0}/_snapshot/weblogs-index-backups/{1}'
                 .format(endpoint, dt_now))
    print('SnapshotName: {}'.format(dt_now))


def delete_old_indices(endpoint, ret_period):
    print('Getting indices older than {} day(s)...'.format(ret_period))

    pattern = '%Y.%m.%d'
    r = requests.get('https://{}/_cat/indices'.format(endpoint))
    indices = []

    for line in r.iter_lines():
        if re.search('logstash', line.decode()) or \
           re.search('cwl', line.decode()):
            indices.append((line.decode().split(' ')[2]))

    for index in indices:
        cur_date = datetime.utcnow().strftime(pattern)
        epoch_cur_date = int(time.mktime(time.strptime(cur_date, pattern)))
        index_date = index.split('-')[1]
        epoch_index_date = int(time.mktime(time.strptime(index_date, pattern)))
        time_diff = int((epoch_cur_date - epoch_index_date) / (60*60*24))

        if time_diff > ret_period:
            print('Removing index: {}...'.format(index))

            r = requests.delete('https://{0}/{1}'.format(endpoint, index))
            ack = json.loads(r.text)['acknowledged']

            if ack is True:
                print('{} has been removed!'.format(index))
            else:
                print('Unable to remove {}!'.format(index))
                print('{0}: {1}'.format(index, json.loads(r.text)))
        else:
            print('Skipping index: {}...'.format(index))


def test_con(endpoint):
    r = requests.get('https://{}'.format(endpoint))

    if r.status_code == 200:
        return True, r.text, r.status_code
    else:
        return False, r.text, r.status_code


def lambda_handler(event, context):
    endpoint = os.environ['ES_ENDPOINT']
    ret_period = os.environ['RET_PERIOD']

    # Test connection
    boolean, msg, status_code = test_con(endpoint)

    if boolean is True:
        print('Connection: OK')
        print('Status: {}'.format(status_code))
    else:
        print(json.loads(msg)['Message'])
        print('Status: {}'.format(status_code))
        sys.exit(1)

    delete_old_indices(endpoint, ret_period)
    create_snapshot(endpoint)
