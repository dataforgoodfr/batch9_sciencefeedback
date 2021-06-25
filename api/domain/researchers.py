from datetime import datetime


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


def return_top_k(authors_dict,k):
    sorted_dict = dict(sorted(authors_dict.items(), key=lambda item: item[1]['score'],reverse=True))
    sorted_dict = dict(list(sorted_dict.items())[:k])
    return sorted_dict


def enrich_authors_dict(authors_dict,articles_dict):
    new_authors_dict = {}
    for values in authors_dict.values():
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
