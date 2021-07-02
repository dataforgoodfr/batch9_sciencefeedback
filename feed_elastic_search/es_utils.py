import xmltodict
import collections
import wget
import numpy as np
import time
import elasticsearch

def add_to_authors_batch(tmp_list_authors,author_subdict):
    tmp_dict = {
        '_op_type':'index',
        '_index':'authors',
        '_type':'author',
        '_id':author_subdict['ConcatId'],
        'LastName':author_subdict['LastName'],
        'FirstName':author_subdict['ForeName'],
        'Initials':author_subdict['Initials'],
        'Affiliations':[],
        'Articles':[]
        }
    tmp_list_authors.append(tmp_dict)
    return tmp_list_authors

def add_to_articles_batch(tmp_list_articles,article_subdict):
    tmp_dict = {'_index':'articles',
            '_type':'article',
            '_id':article_subdict['pmid'],
            'doi':article_subdict['doi'],
            'title':article_subdict['title'],
            'abstract':article_subdict['abstract'],
            'journal':article_subdict['journal']['NlmUniqueID'],
            'date':int(article_subdict['date'].timestamp()),
            'authors':[author['ConcatId'] for author in article_subdict['authors']],
            'keywords':article_subdict['keywords'],
            }
    tmp_list_articles.append(tmp_dict)
    return tmp_list_articles

def add_to_journals_batch(tmp_list_journals,articles_subdict,issn_linking):
    tmp_dict = {
        '_index':'journals',
        '_type':'journal',
        '_id':articles_subdict['journal']['NlmUniqueID'],
        'FullTitle':articles_subdict['journal']['FullName'],
        'MedlineTA':articles_subdict['journal']['MedlineTA'],
        'ISSN':issn_linking,
        }
    tmp_list_journals.append(tmp_dict)
    return tmp_list_journals 

def add_to_author_article_batch(tmp_list_author_articles,article_id,author_subdict):
    tmp_dict = {
            '_op_type': 'update',
            '_index': 'authors',
            '_type': 'author',
            '_id': author_subdict['ConcatId'],
            "script" : {
                "source": "if (!ctx._source.Articles.contains(params.articleid)){ctx._source.Articles.add(params.articleid)}",
                "lang": "painless",
                "params" : {"articleid" : article_id}
                    }
            }
    tmp_list_author_articles.append(tmp_dict)
    return tmp_list_author_articles

def add_to_author_affils_batch(tmp_list_author_affils,author_subdict,affil):
    tmp_dict = {
                '_op_type': 'update',
                '_index': 'authors',
                '_type': 'author',
                '_id': author_subdict['ConcatId'],
                "script" : {
                    "source": "if (!ctx._source.Affiliations.contains(params.affiliation)){ctx._source.Affiliations.add(params.affiliation)}",
                    "lang": "painless",
                    "params" : {"affiliation" : affil}
                        }
                }

    tmp_list_author_affils.append(tmp_dict)
    return tmp_list_author_affils

def upload_keyword_info(lst_keywords,article_id,es):
    for keyword in lst_keywords:
        tmp_dict = {'_op_type':'index','Articles':[],'biobert_embedding' : np.array([0.0]*768)}
        try:
            es.index(index='keywords',body = tmp_dict,id=str(keyword)[:500])
        except Exception as e:
            print(e)
            print('error on keyword indexing, retrying in 30 secs')
            time.sleep(30)
            try:
                es.index(index='keywords',body = tmp_dict,id=str(keyword)[:500])
            except Exception as e:
                print(e)
                print('New Exception when adding keywords')
                time.sleep(30)
                continue
        
        query = {'script': {'source': 'if (!ctx._source.Articles.contains(params.articleid)){ctx._source.Articles.add(params.articleid)}',
                'lang': 'painless',
                'params': {'articleid': article_id}}}
        try:
            es.update(index='keywords',id=str(keyword)[:500],body=query)
        except Exception as e:
            print(e)
            print('error on keyword-article linking, retrying in 5 secs')
            time.sleep(30)
            try:
                es.update(index='keywords',id=str(keyword)[:500],body=query)
            except Exception as e:
                print(e)
                print('New Exception when mapping keywords and articles')
                time.sleep(30)
                continue




def process_master_dict(master_dict,es):
    tmp_list_articles = []
    tmp_list_journals = []
    tmp_list_authors = []
    tmp_list_author_articles = []
    tmp_list_author_affils = []

    counter = 0
    for key,values in master_dict.items():
        counter+=1
        print(counter,end='\r')

        #preprocessing hacks
        if isinstance(values['title'],collections.OrderedDict):
            values['title'] = values['title']['#text']
        if 'ISSNLinking' in values['journal']:
            issn_linking = values['journal']['ISSNLinking']
        else:
            issn_linking=None

        #prepare batches
        tmp_list_articles = add_to_articles_batch(tmp_list_articles,values)
        tmp_list_journals = add_to_journals_batch(tmp_list_journals,values,issn_linking)

        for author_subdict in values['authors']:
            tmp_list_authors = add_to_authors_batch(tmp_list_authors,author_subdict)
            tmp_list_author_articles = add_to_author_article_batch(tmp_list_author_articles,values['pmid'],author_subdict)

            for affil in author_subdict['AffiliationInfo']:
                tmp_list_author_affils = add_to_author_affils_batch(tmp_list_author_affils,author_subdict,affil)

        # upload keywords one by one (cannot be batched for a knn index upload)
        if values['keywords']:
            upload_keyword_info(values['keywords'],values['pmid'],es)

    return tmp_list_articles,tmp_list_journals,tmp_list_authors,tmp_list_author_articles,tmp_list_author_affils


def reset_database(es):
    es.indices.delete('articles')
    es.indices.delete('journals')
    es.indices.delete('authors')
    es.indices.delete('keywords')
    query = {"settings": {"index.knn": True,"knn.space_type": "cosinesimil"},
                        "mappings": {
                            "properties": {
                                "biobert_embedding": {
                                    "type": "knn_vector",
                                    "dimension": 768},
                        }}}

    es.indices.create(index='keywords',body=query)
