from domain.researchers import add_article_subdict_to_dict, \
                               enrich_authors_dict, \
                               return_top_k
from utils.search import CLIENT


def convert_journal_ids_to_names(authors_dict):
    set_journal_ids = set([])
    for values in authors_dict.values():
        for article in values['Articles']:
            set_journal_ids.update([article['Journal']])

    res = CLIENT.mget(body={"ids" : list(set_journal_ids)}, index='journals')['docs']
    dict_names = {elem['_id']:elem['_source']['FullTitle'] for elem in res}

    for values in authors_dict.values():
        for article in values['Articles']:
            article['Journal'] = dict_names[article['Journal']]
    return authors_dict


def get_article_ids(lst_keywords):
    set_articles = set()
    res = CLIENT.mget(body={"ids" : lst_keywords}, index='copy-keywords')
    for keyword in res['docs']:
        for article in keyword['_source']['Articles']:
            set_articles.update([article])
    return set_articles


def get_articles_info(set_articles):
    authors_dict = {}
    articles_dict = {}

    res = CLIENT.mget(body={"ids" : list(set_articles)}, index='articles')
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


def get_authors_info(authors_dict):
    lst_authors = list(authors_dict.keys())
    res = CLIENT.mget(body={"ids" : lst_authors}, index='authors')
    for author in res['docs']:
        authors_dict[author['_id']]['Name'] = author['_source']['FirstName'] + ' ' + author['_source']['LastName']
        authors_dict[author['_id']]['Affiliations'] = author['_source']['Affiliations']
    return authors_dict


def researchers_from(keywords, k):
    set_articles = get_article_ids(keywords)
    authors_dict,articles_dict = get_articles_info(set_articles)
    authors_dict = get_authors_info(authors_dict)
    authors_dict = return_top_k(authors_dict,k)
    authors_dict = enrich_authors_dict(authors_dict,articles_dict)
    authors_dict = convert_journal_ids_to_names(authors_dict)
    return authors_dict
