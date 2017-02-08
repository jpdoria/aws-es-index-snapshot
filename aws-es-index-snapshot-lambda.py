# AWS Documentation: https://goo.gl/0wpSJm

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
        difference = (epoch_cur_date - epoch_index_date) / (60*60*24)
        time_diff = int(difference)

        if time_diff > ret_period:
            print('Removing index: {}...'.format(index))
            requests.delete('https://{0}/{1}'.format(endpoint, index))
            print('{} has been removed!'.format(index))
        else:
            print('Skipping index: {}...'.format(index))


def lambda_handler(event, context):
    endpoint = os.environ['ES_ENDPOINT']
    ret_period = os.environ['RET_PERIOD']

    delete_old_indices(endpoint, ret_period)
    create_snapshot(endpoint)
