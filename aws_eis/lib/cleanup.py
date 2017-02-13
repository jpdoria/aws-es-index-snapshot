import json
import re
import time
import requests
from datetime import datetime


def cleanup(args):
    endpoint = args.endpoint
    ret_period = int(args.retention_period)
    pattern = '%Y.%m.%d'
    r = requests.get('https://{}/_cat/indices'.format(endpoint))
    indices = []

    for line in r.iter_lines():
        if re.search('logstash', line.decode()) or \
         re.search('cwl', line.decode()):
            indices.append(line.decode().split(' ')[2])

    for index in indices:
        cur_date = datetime.now().strftime(pattern)
        epoch_cur_date = int(time.mktime(time.strptime(cur_date, pattern)))
        index_date = index.split('-')[1]
        epoch_index_date = int(time.mktime(time.strptime(index_date, pattern)))
        time_diff = int((epoch_cur_date - epoch_index_date) / (60*60*24))

        if time_diff > ret_period:
            print('Removing {}...'.format(index))

            r = requests.delete('https://{0}/{1}'.format(endpoint, index))
            ack = json.loads(r.text)['acknowledged']

            if ack is True:
                print('{} has been removed!'.format(index))
            else:
                print('Unable to remove {}!'.format(index))
        else:
            print('Skipping {}...'.format(index))
