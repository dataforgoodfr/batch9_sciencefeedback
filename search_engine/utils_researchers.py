from elasticsearch import Elasticsearch,helpers
import json
import numpy as np
from datetime import datetime

def get_article_ids(lst_keywords,es):
    set_articles = set()
    res = es.mget(body={"ids" : lst_keywords}, index='copy-keywords')
    for keyword in res['docs']:
        for article in keyword['_source']['Articles']:
            set_articles.update([article])
    return set_articles

def add_article_subdict_to_dict(article_subdict,articles_dict):
    articles_dict[article_subdict['_id']] = {'id' : article_subdict['_id'],
                                             'doi' : 'https://doi.org/'+article_subdict['_source']['doi'],
                                             'abstract' : article_subdict['_source']['abstract'],
                                             'title' : article_subdict['_source']['title'],
                                             'journal' : article_subdict['_source']['journal'],
                                             'abstract' : article_subdict['_source']['abstract'],
                                             'date' : datetime.fromtimestamp(article_subdict['_source']['date'])
                                            }
    return articles_dict
    
def get_articles_info(set_articles,es):
    authors_dict = {}
    articles_dict = {}
    
    res = es.mget(body={"ids" : list(set_articles)}, index='articles')
    for article in res['docs']:
        try:
            articles_dict = add_article_subdict_to_dict(article,articles_dict)
            authors = article['_source']['authors']
            if authors:
                for idx,author in enumerate(authors):
                    if author in authors_dict:
                        authors_dict[author]['articles'].append(article['_id'])
                        if idx == 0:
                            authors_dict[author]['score'] += 4
                        else:
                            authors_dict[author]['score'] += 1
                    else:
                        if idx == 0:
                            authors_dict[author] = {'score' : 4,'articles':[article['_id']]}
                        if idx != 0:
                            authors_dict[author] = {'score' : 1,'articles':[article['_id']]}
        except (KeyError,TypeError):
            pass

    return authors_dict,articles_dict

def get_authors_info(authors_dict,es):
    lst_authors = list(authors_dict.keys())
    res = es.mget(body={"ids" : lst_authors}, index='authors')
    for author in res['docs']:
        authors_dict[author['_id']]['Name'] = author['_source']['FirstName'] + ' ' + author['_source']['LastName']
        authors_dict[author['_id']]['Affiliations'] = author['_source']['Affiliations']
    return authors_dict
 
def return_top_k(authors_dict,k):
    sorted_dict = dict(sorted(authors_dict.items(), key=lambda item: item[1]['score'],reverse=True))
    sorted_dict = dict(list(sorted_dict.items())[:k])
    return sorted_dict    


def convert_journal_ids_to_names(authors_dict,es):
    set_journal_ids = set([])
    for key,values in authors_dict.items():
        for article in values['Articles']:
            set_journal_ids.update([article['Journal']])
    
    res = es.mget(body={"ids" : list(set_journal_ids)}, index='journals')['docs']
    dict_names = {elem['_id']:elem['_source']['FullTitle'] for elem in res}
    
    for key,values in authors_dict.items():
        for article in values['Articles']:
            article['Journal'] = dict_names[article['Journal']]
    return authors_dict

def enrich_authors_dict(authors_dict,articles_dict):
    new_authors_dict = {}
    for key,values in authors_dict.items():
        new_authors_dict[values['Name']] = {'Affiliations':values['Affiliations'],
                                           'Score':values['score'],
                                           'Articles':[]
                                           }
        for article in values['articles']:
            temp_dict = {'doi':articles_dict[article]['doi'],
                        'PublicationDate':str(articles_dict[article]['date'].year)+'-'
                                         +str(articles_dict[article]['date'].month)+'-'
                                         +str(articles_dict[article]['date'].day),
                        'Title':articles_dict[article]['title'],
                        'Journal':articles_dict[article]['journal'],
                        'Abstract':articles_dict[article]['abstract'],
                        }
            new_authors_dict[values['Name']]['Articles'].append(temp_dict)  
            
    return new_authors_dict

def wrapper_researchers(lst_keywords,k,es):
    set_articles = get_article_ids(lst_keywords,es)
    authors_dict,articles_dict = get_articles_info(set_articles,es)
    authors_dict = get_authors_info(authors_dict,es)
    authors_dict = return_top_k(authors_dict,k)
    authors_dict = enrich_authors_dict(authors_dict,articles_dict)
    autors_dict = convert_journal_ids_to_names(authors_dict,es)
    return authors_dict
