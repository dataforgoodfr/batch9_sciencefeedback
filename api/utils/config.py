import os
from logging import INFO as LOG_LEVEL_INFO
from pathlib import Path
import sys


APP_NAME = os.environ.get('APP_NAME', '')
COMMAND_NAME = os.environ.get('COMMAND_NAME', '')
COMPOSITION = os.environ.get('COMPOSITION', 'serve-development')
NGROK_API_SUBDOMAIN = os.environ.get('NGROK_API_SUBDOMAIN', '')
NGROK_WEBAPP_SUBDOMAIN = os.environ.get('NGROK_WEBAPP_SUBDOMAIN', '')
PLATFORM = os.environ.get('PLATFORM', '')
PORT = int(os.environ.get('PORT', 5000))
TLD = os.environ.get('TLD', '')
WEBAPP_SUBDOMAIN = os.environ.get('WEBAPP_SUBDOMAIN', '')

API_ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__))) / '..'

VERSION_FILE = open(os.path.join(API_ROOT_PATH, 'version.txt'), 'r')
VERSION = VERSION_FILE.read().rstrip()
VERSION_FILE.close()

MACHINE_ENV = os.environ.get('MACHINE_ENV', 'development')
IS_DEVELOPMENT = MACHINE_ENV == 'development'
IS_PRODUCTION = MACHINE_ENV == 'production'

LOG_LEVEL = int(os.environ.get('LOG_LEVEL', LOG_LEVEL_INFO))

IS_CHECKHEALTH = sys.argv[0] == 'checkhealth.py'
IS_SCHEDULER = sys.argv[0].endswith('celery') \
               and len(sys.argv) > 3 and \
               sys.argv[2] == 'beat'
IS_WORKER = sys.argv[0].endswith('celery') \
            and len(sys.argv) > 3 \
            and sys.argv[2] == 'worker'
IS_APP = not IS_CHECKHEALTH and not IS_SCHEDULER and not IS_WORKER


if IS_DEVELOPMENT:
    if PLATFORM == 'ngrok':
        API_URL = 'https://{}.ngrok.io'.format(NGROK_API_SUBDOMAIN)
        WEBAPP_URL = 'https://{}.ngrok.io'.format(NGROK_WEBAPP_SUBDOMAIN)
    else:
        API_URL = 'http://apiweb-{}:5000'.format(COMPOSITION)
    WEBAPP_URL = 'http://localhost:3000'
elif IS_PRODUCTION:
    API_URL = 'https://api.{}.{}'.format(APP_NAME, TLD)
    WEBAPP_URL = 'https://{}.{}'.format(APP_NAME, TLD)
else:
    API_URL = 'https://api-{}.{}.{}'.format(MACHINE_ENV, APP_NAME, TLD)
    WEBAPP_URL = 'https://{}-{}.{}.{}'.format(WEBAPP_SUBDOMAIN, MACHINE_ENV, APP_NAME, TLD)

DEFAULT_USER_PASSWORD = os.environ.get('DEFAULT_USER_PASSWORD', '')
