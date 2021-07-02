import os
import elasticsearch


ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST')
ELASTICSEARCH_PASSWORD = os.environ.get('ELASTICSEARCH_PASSWORD')
ELASTICSEARCH_UNAME = os.environ.get('ELASTICSEARCH_UNAME')


def client_from():
    if ELASTICSEARCH_UNAME and ELASTICSEARCH_PASSWORD and ELASTICSEARCH_HOST:
        return elasticsearch.Elasticsearch(ELASTICSEARCH_HOST,
                                           http_auth=(ELASTICSEARCH_UNAME, ELASTICSEARCH_PASSWORD),
                                           timeout=30,
                                           max_retries=30,
                                           retry_on_timeout=True)
    return None

CLIENT = client_from()
