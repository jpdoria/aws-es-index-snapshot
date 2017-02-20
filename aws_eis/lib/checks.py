import json
import sys
import requests


def py_version():
    if sys.version_info < (3, 0, 0):
        print(sys.version)
        print('You must use Python 3.x to run this application.')
        sys.exit(1)


def get_version(endpoint):
    r = requests.get('https://{}'.format(endpoint))
    es_version = json.loads(r.text)['version']['number']

    return es_version


def test_con(endpoint):
    r = requests.get('https://{}'.format(endpoint))

    try:
        es_version = get_version(endpoint)
    except KeyError:
        print('Status: {}'.format(r.status_code))
        sys.exit(1)
    else:
        if r.status_code == 200:
            print('ESVersion: {}'.format(es_version))
            print('Connection: OK')
            print('Status: {}\n'.format(r.status_code))
