import json
import os

conf = os.path.join(os.path.expanduser('~'), '.gwt')

if not os.path.exists(conf):
    raise OSError(
        '{} does not exist. View README for more information.'.format(conf)
    )

with open(conf, 'rb') as f:
    creds = json.loads(f.read())
