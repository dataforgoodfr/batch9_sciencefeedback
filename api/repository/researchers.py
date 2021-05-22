import pickle

from models.researcher import Researcher
from utils.database import db
from utils.tmp import PATH as TMP_PATH


PICKLES_PATH = TMP_PATH / 'pickles'

with open(PICKLES_PATH / 'dict_authors_v3.pickle', 'rb') as handle:
    dict_authors = pickle.load(handle)


def add_to_lst_researchers(value_researcher, key, top_k_researchers):
    top_k_researchers = sorted(top_k_researchers, key=lambda x: x[1],reverse=False)
    if value_researcher > top_k_researchers[0][1]:
        top_k_researchers[0][0] = key
        top_k_researchers[0][1] = value_researcher
    return top_k_researchers


def researchers_from(keywords, k):

    # METHOD TO BE IMPLEMENTED WITH THE DATABASE
    # return Reviewer.query.filter(...).all()

    top_k_researchers = [['',0] for _ in range(k)]
    for key,values in dict_authors.items():
        value_researcher = 0
        for keyword in keywords:
            if keyword in values['Keywords']:
                value_researcher += values['Keywords'][keyword]
        top_k_researchers = add_to_lst_researchers(value_researcher, key, top_k_researchers)
    top_k_researchers = sorted(top_k_researchers, key=lambda item: item[1], reverse=True)

    for researcher in top_k_researchers:
        researcher.append([elem['Title'] for elem in dict_authors[researcher[0]]['Articles']])
    return top_k_researchers


def create_or_modify_researcher(datum):
    researcher = Researcher.query.filter_by(email=datum['email']).first()
    if not researcher:
        researcher = Researcher()
    for (key, value) in datum.items():
        setattr(researcher, key, value)
    db.session.add(researcher)
    return researcher
