#!/usr/bin/env python
import os
import sys

import time
import es_utils
import parse_pubmed_data_utils
import secrets
import elasticsearch
from elasticsearch import helpers

host = "https://search-feedback-yk5vieg43b7y34n27afc7ebbvq.eu-west-3.es.amazonaws.com"
uname = 'feedback'
password = 'oWwu3B6jWqG;fgS'
es = elasticsearch.Elasticsearch(secrets.host,http_auth=(secrets.uname,secrets.password),
                                timeout=30,
                                max_retries=30,
                                retry_on_timeout=True,
                                )

#uncomment the function below if you need to reset the database
#es_utils.reset_database(es)


def main(nb_start_doc):
    for doc_number in range(nb_start_doc,1055):
        # download a bunch (~30k articles) of data from pubmed and parse it into a dict
        master_dict = parse_pubmed_data_utils.wrapper_download_and_turn_to_dict(doc_number)

        # create elasticsearch batch queries from dict and upload items that can't be batched
        tmp_list_articles,tmp_list_journals,tmp_list_authors,tmp_list_author_articles,tmp_list_author_affils = es_utils.process_master_dict(master_dict,es)
        
        #upload batches
        for upload_lst in [tmp_list_articles,tmp_list_journals,tmp_list_authors,tmp_list_author_articles,tmp_list_author_affils]:
            try:
                elasticsearch.helpers.bulk(es,upload_lst)
            except Exception as e:
                print(e)
                print('Bulktimeout error, trying again in 30 secs')
                time.sleep(30)
                try:
                    helpers.bulk(es,upload_lst)
                except Exception as e:
                    print('NewBulkError, moving on')
                    time.sleep(30)
                    continue

        #refresh indices to reduce chances of crashing 
        for index_name in ['authors','articles','keywords','journals']:
            try:
                es.indices.refresh(index_name,request_timeout=150)
            except Exception as e:
                print(e)
                print('Index refresh error, trying again in 30 secs')
                time.sleep(30)
                es.indices.refresh(index_name,request_timeout=150)

        # save the file number of the latest processed file to be able to pick up where we left off in case of program crash
        with open('counter.txt','w') as file:
            file.write(str(doc_number+1))


# get the file number of the file downloaded to pick up where we left off
with open('counter.txt','r') as file:
    nb_start_doc = int(file.read().strip())

if __name__ == '__main__':
    try:
        main(nb_start_doc)
    except Exception as e:
        print("PROGRAM FAILED, RESTARTING",e)
        time.sleep(30)
        os.execv(__file__,sys.argv)
