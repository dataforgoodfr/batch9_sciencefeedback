import pickle
from sklearn.metrics.pairwise import cosine_similarity

from utils.nlp import tokenize_string
from utils.tmp import PATH as TMP_PATH

PICKLES_PATH = TMP_PATH / 'pickles'


with open(PICKLES_PATH / 'keywords_and_vectors_v4.pkl', 'rb') as handle:
    dict_vectors = pickle.load(handle)
lst_remove = [key for key in dict_vectors.keys() if key=='']
for elem in lst_remove:
    dict_vectors.pop(elem)


with open(PICKLES_PATH / 'keyword_similarity_v2.pkl', 'rb') as handle:
    dict_simil = pickle.load(handle)


with open(PICKLES_PATH  / 'neighbor_model.pkl','rb') as handle:
    neighbor_model = pickle.load(handle)


def keywords_from(search_query,
                  max_distance=10,
                  similarity_threshold=0.5):
    vector = tokenize_string(search_query)
    prelim_kw = preliminary_keywords_from(vector, max_distance)
    interm_kw = intermediate_keywords_from(prelim_kw, similarity_threshold)
    final_kw = final_list_keywords_from(interm_kw)
    return final_kw


def final_list_keywords_from(intermediate_lst_keywords):
    final_lst_keywords = []
    for intermediate_keyword in intermediate_lst_keywords:
        final_lst_keywords.extend(dict_simil[intermediate_keyword])
    return list(set(final_lst_keywords))


def intermediate_keywords_from(preliminary_lst_keywords,
                               similarity_threshold=.985):
    intermediate_lst_keywords = []
    for keyword in preliminary_lst_keywords:
        vec1 = dict_vectors[keyword]
        lst_cos_sim = []
        for intermediate_keyword in intermediate_lst_keywords:
            vec2 = dict_vectors[intermediate_keyword]
            cos_sim = cosine_similarity(vec1.reshape(1,-1),vec2.reshape(1,-1))[0][0]
            lst_cos_sim.append(cos_sim)
        if all(cos_sim<similarity_threshold for cos_sim in lst_cos_sim):
            intermediate_lst_keywords.append(keyword)
    return intermediate_lst_keywords


def preliminary_keywords_from(vector,
                              max_distance=6):
    twenty_nearest_neighbors = neighbor_model.kneighbors(vector.reshape(1,-1))
    preliminary_lst_keywords = []

    for distance,pos in zip(twenty_nearest_neighbors[0][0],twenty_nearest_neighbors[1][0]):
        if distance < max_distance:
            preliminary_lst_keywords.append(list(dict_vectors.keys())[pos])

    return preliminary_lst_keywords
