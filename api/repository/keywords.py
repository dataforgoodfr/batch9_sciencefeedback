from utils.search import CLIENT

# TODO FROM torchserve
# biobert_tokenizer = AutoTokenizer.from_pretrained('dmis-lab/biobert-v1.1')
# biobert_model = AutoModel.from_pretrained('dmis-lab/biobert-v1.1')

def vectorize_string(string):
    # token_keyword = torch.tensor(biobert_tokenizer.encode(string)).unsqueeze(0)
    # out = biobert_model(token_keyword)
    # TODO adapt out with torchserve
    out = [[string]]
    vector = out[0][0][1:-1].detach().numpy().mean(axis=0).tolist()
    return vector

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
