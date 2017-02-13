import json
import sys
import requests


def restore(args):
    endpoint = args.endpoint
    snap_name = args.snapshot_name

    print('Note: you cannot restore a snapshot of your indices to an ' +
          'Elasticsearch cluster that already contains indices with ' +
          'the same names. Currently, Amazon ES does not support ' +
          'the Elasticsearch _close API, so you must use one of the ' +
          'following alternatives:\n\n' +
          '1. Delete the indices on the {}, '.format(endpoint) +
          'then restore the snapshot\n' +
          '2. Restore the snapshot to a different Amazon ES domain\n')

    while True:
        try:
            choice = int(input('Choose an option: [1/2] '))
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit(1)
        except ValueError as e:
            print('Please choose between 1 and 2.')
        else:
            if choice == 1:
                print('Deleting indices on {}...'.format(endpoint))

                r = requests.delete('https://{}/_all'.format(endpoint))
                ack = json.loads(r.text)['acknowledged']

                if ack is True:
                    print('Indices have been removed!')
                else:
                    print('Unable to remove indices!')
                    sys.exit(1)

                snap_dir = '_snapshot/weblogs-index-backups/'

                print('Restoring {}...'.format(snap_name))

                r = requests.post(
                    'https://{0}/{1}/{2}/_restore?'
                    .format(endpoint, snap_dir, snap_name)
                )

                if r.status_code == 200:
                    print('Success! Please allow time for complete ' +
                          'restoration.'.format(snap_name))
                    sys.exit(0)
                else:
                    print(r.text)
                    sys.exit(1)
            elif choice == 2:
                url = 'https://{}/_snapshot/weblogs-index-backups'.format(
                        endpoint)

                r = requests.get(url)
                bucket_name = json.loads(r.text)[
                    'weblogs-index-backups']['settings']['bucket']

                print('\nSnapshotDirectory: weblogs-index-backups')
                print('S3Bucket: {}\n'.format(bucket_name))
                print('Please register the snapshot directory to ' +
                      'your new Amazon Elasticsearch Service domain ' +
                      'then execute \'restore\' again.')
            else:
                print('Please choose between 1 and 2.')
