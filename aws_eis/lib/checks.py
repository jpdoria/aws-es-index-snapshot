import json
import requests


def get_version(endpoint):
    r = requests.get('https://{}'.format(endpoint))
    es_version = json.loads(r.text)['version']['number']

    return es_version


def test_con(endpoint):
    r = requests.get('https://{}'.format(endpoint))
    es_version = get_version(endpoint)

    if r.status_code == 200:
        print('ESVersion: {}'.format(es_version))
        print('Connection: OK')
        print('Status: {}\n'.format(r.status_code))
    else:
        print(json.loads(msg)['Message'])
        print('Status: {}'.format(status_code))
        sys.exit(1)
