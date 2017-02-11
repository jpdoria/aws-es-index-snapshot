import json
import requests


def get_version(endpoint):
    r = requests.get('https://{}'.format(endpoint))
    es_version = json.loads(r.text)['version']['number']

    return es_version


def test_con(endpoint):
    r = requests.get('https://{}'.format(endpoint))

    if r.status_code == 200:
        return True, r.text, r.status_code
    else:
        return False, r.text, r.status_code
