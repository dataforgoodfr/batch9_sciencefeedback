from transformers import AutoModel, AutoTokenizer
import torch


scibert_tokenizer = AutoTokenizer.from_pretrained('dmis-lab/biobert-v1.1')
scibert_model = AutoModel.from_pretrained('dmis-lab/biobert-v1.1')


def tokenize_string(string):
    token_keyword = torch.tensor(scibert_tokenizer.encode(string)).unsqueeze(0)
    out = scibert_model(token_keyword)
    vector = out[0][0][1:-1].detach().numpy().mean(axis=0)
    return vector
