import os
import json
import requests
from requests.auth import HTTPBasicAuth

from utils.config import COMPOSITION


LOCALHOST_TORCHSERVE_URL = 'http://torchserve-{}:8080'.format(COMPOSITION)
TORCHSERVE_URL = os.environ.get('TORCHSERVE_URL', LOCALHOST_TORCHSERVE_URL)

HEADERS = {
    'Accept':'application/json',
    'Content-Type': 'application/json'
}

AUTH = HTTPBasicAuth('infra',
                     os.environ.get('NLPDATA_INFRA_HTPASSWD'))


def ping():
    return requests.get(f'{TORCHSERVE_URL}/ping', auth=AUTH).json()


def vectors_from_sentences(sentences,
                           model_name='stsbrobertabase'):
    response = requests.post(f'{TORCHSERVE_URL}/predictions/{model_name}',
                             auth=AUTH,
                             data=json.dumps(sentences),
                             headers=HEADERS)

    result = json.loads(response.content.decode('utf8'))

    if 'embedding' in result:
        return result['embedding']

    error_message = result['error']
    raise 'Torchserve error' + str(error_message)
