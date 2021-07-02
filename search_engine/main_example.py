from elasticsearch import Elasticsearch
import utils_keywords
import utils_researchers

user_query = 'ivermectin tolerance'
tolerance_synonyms = 5
number_researchers = 10

host = "XXX"
uname = 'XXX'
password = 'XXX'

es = Elasticsearch(host=host,
                    http_auth=(uname,password),
                    timeout=30,
                    max_retries=30,
                    retry_on_timeout=True,
                    )

lst_keywords = utils_keywords.keywords(user_query,tolerance_synonyms,es)
dict_authors = utils_researchers.wrapper_researchers(lst_keywords,number_researchers,es)