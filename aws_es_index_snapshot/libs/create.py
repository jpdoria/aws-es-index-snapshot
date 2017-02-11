import hashlib
import requests

from datetime import datetime


def create(args):
    endpoint = args.endpoint
    dt_now = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    m = hashlib.md5()
    m.update(dt_now.encode())
    snap_hash = m.hexdigest()
    snap_name = '{0}-{1}'.format(dt_now, snap_hash)

    print('Creating snapshot...')
    requests.put('https://{0}/_snapshot/weblogs-index-backups/{1}'
                 .format(endpoint, snap_name))
    print('SnapshotName: {}'.format(snap_name))
