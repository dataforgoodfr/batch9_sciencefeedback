from transformers import AutoModel, AutoTokenizer
import torch

from utils.nlp import vectorize_string
from utils.search import CLIENT


def keywords_from(search_query, min_score):
    min_score = .9 + min_score/100
    query = {"size": 50,
             "min_score" : min_score,
             "_source" : 'false',
             "query": {
                 "knn": {
                     "biobert_embedding": {
                        "vector": vectorize_string(search_query),
                        "k": 50
            }}}}
    res = CLIENT.search(index='copy-keywords',body=query,timeout='500s')

    lst_results = [result['_id'] for result in res['hits']['hits']]
    return lst_results
