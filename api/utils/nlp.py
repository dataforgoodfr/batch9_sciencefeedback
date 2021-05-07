from transformers import *
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from pathlib import Path

PICKLES_PATH = Path(os.path.dirname(os.path.realpath(__file__))+ '/../tmp/pickles')
print(os.getcwd())
with open('./tmp/pickles/keywords_and_vectors_v4.pkl', 'rb') as handle:
    dict_vectors = pickle.load(handle)
print('hello')
'''
lst_remove = [key for key in dict_vectors.keys() if key=='']
for elem in lst_remove:
    dict_vectors.pop(elem)

with open('keyword_similarity_v2.pkl', 'rb') as handle:
    dict_simil = pickle.load(handle)
    
with open('dict_authors_v3.pickle', 'rb') as handle:
    dict_authors = pickle.load(handle)

with open('neighbor_model.pkl','rb') as handle:
    neighbor_model = pickle.load(handle)

scibert_tokenizer = AutoTokenizer.from_pretrained('dmis-lab/biobert-v1.1')
scibert_model = AutoModel.from_pretrained('dmis-lab/biobert-v1.1')


def tokenize_string(string):
    token_keyword = torch.tensor(scibert_tokenizer.encode(string)).unsqueeze(0)
    out = scibert_model(token_keyword)
    vector = out[0][0][1:-1].detach().numpy().mean(axis=0)
    return vector

def get_preliminary_keywords(vector,max_distance=6):
    twenty_nearest_neighbors = neighbor_model.kneighbors(vector.reshape(1,-1))
    preliminary_lst_keywords = []

    for distance,pos in zip(twenty_nearest_neighbors[0][0],twenty_nearest_neighbors[1][0]):
        if distance < max_distance:
            preliminary_lst_keywords.append(list(dict_vectors.keys())[pos])
            
    return preliminary_lst_keywords

def get_intermediate_keywords(preliminary_lst_keywords,similarity_threshold=.985):
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

def get_final_list_keywords(intermediate_lst_keywords):
    final_lst_keywords = []
    for intermediate_keyword in intermediate_lst_keywords:
        final_lst_keywords.extend(dict_simil[intermediate_keyword])
    return list(set(final_lst_keywords))

def add_to_lst_scientists(value_scientist,key,top_k_scientists):
    top_k_scientists = sorted(top_k_scientists, key=lambda x: x[1],reverse=False)
    if value_scientist > top_k_scientists[0][1]:
        top_k_scientists[0][0] = key
        top_k_scientists[0][1] = value_scientist
    return top_k_scientists

def get_keywords(search_query,max_distance,similarity_threshold):
    vector = tokenize_string(search_query)
    prelim_kw = get_preliminary_keywords(vector,max_distance)
    interm_kw = get_intermediate_keywords(prelim_kw,similarity_threshold)
    final_kw = get_final_list_keywords(interm_kw)
    return final_kw

def get_scientists(keywords,k):
    top_k_scientists = [['',0] for _ in range(k)]
    for key,values in dict_authors.items():
        value_scientist = 0
        for keyword in keywords:
            if keyword in values['Keywords']:
                value_scientist += values['Keywords'][keyword]
        top_k_scientists = add_to_lst_scientists(value_scientist,key,top_k_scientists)
    top_k_scientists = sorted(top_k_scientists, key=lambda item: item[1],reverse=True)
    
    for scientist in top_k_scientists:
        scientist.append([elem['Title'] for elem in dict_authors[scientist[0]]['Articles']])
    return top_k_scientists
'''