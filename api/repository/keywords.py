from utils.search import CLIENT


def keywords_from():
    return CLIENT.search(index="researchers", body={"query": {"match_all": {}}})
