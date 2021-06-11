#!/usr/bin/env python
import os
import sys

import time
import es_utils
import parse_pubmed_data_utils
import secrets
import elasticsearch
from elasticsearch import helpers
import requests
import json

es = elasticsearch.Elasticsearch(secrets.host,http_auth=(secrets.uname,secrets.password),
                                timeout=30,
                                max_retries=30,
                                retry_on_timeout=True,
                                )
headers = {'Content-Type': 'application/json'}
print(es.indices.get_alias("*"))
#uncomment the function below if you need to reset the database
#es_utils.reset_database(es)
#print('done')

def main(nb_start_doc):
    for doc_number in range(nb_start_doc,1055):
        # download a bunch (~30k articles) of data from pubmed and parse it into a dict
        master_dict = parse_pubmed_data_utils.wrapper_download_and_turn_to_dict(doc_number)

        # create elasticsearch batch queries from dict and upload items that can't be batched
        tmp_list_articles,tmp_list_journals,tmp_list_authors,tmp_list_author_articles,tmp_list_author_affils,tmp_list_keywords,tmp_list_keywords_articles = es_utils.process_master_dict(master_dict)
        
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
        
        print('uploaded bulks')
        
        for upload_lst in [tmp_list_keywords,tmp_list_keywords_articles]:
            for lst in es_utils.grouper(4000, upload_lst):
                with open('tmp_dump_batch.json', 'w') as fp:
                    fp.write('\n'.join(json.dumps(i) for i in lst) +'\n')
                    fp.write('\n')
                with open('tmp_dump_batch.json', 'rb') as file:
                    data = file.read()
                try:
                    requests.post(secrets.host+'/_bulk', headers=headers, data=data, auth=(secrets.uname,secrets.password),timeout=60)
                except Exception as e:
                    print('Exception when uploading keyword bulk',e)
                    print(data[0])
                    time.sleep(30)
                    try:
                        requests.post(secrets.host+'/_bulk', headers=headers, data=data, auth=(secrets.uname,secrets.password),timeout=60)
                    except Exception as e:
                        print('Exception when uploading keyword bulk',e)
                        print(data[0])
                        time.sleep(30)
        print('uploaded keyword bulks')

        # save the file number of the latest processed file to be able to pick up where we left off in case of program crash
        with open('counter.txt','w') as file:
            file.write(str(doc_number+1))
            

        #refresh indices to reduce chances of crashing 
        for index_name in ['authors','articles','keywords','journals']:
            try:
                es.indices.refresh(index_name,request_timeout=150)
            except Exception as e:
                print(e)
                print('Index refresh error, trying again in 30 secs')
                time.sleep(30)
                es.indices.refresh(index_name,request_timeout=150)


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