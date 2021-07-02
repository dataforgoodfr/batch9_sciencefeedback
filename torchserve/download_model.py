import transformers
from pathlib import Path
import os
import json
import torch
from transformers import AutoTokenizer, AutoModel


print(f'PyTorch version: {torch.__version__}')

NEW_DIR = "./sentence_model"
try:
  os.mkdir(NEW_DIR)
except OSError:
  print ("Creation of directory %s failed" % NEW_DIR)


biobert_tokenizer = AutoTokenizer.from_pretrained('dmis-lab/biobert-v1.1')
biobert_model = AutoModel.from_pretrained('dmis-lab/biobert-v1.1')

biobert_tokenizer.save_pretrained(NEW_DIR)
biobert_model.save_pretrained(NEW_DIR)
print("model is saved")

#loaded_xformer = SentenceTransformer(NEW_DIR)
#print("model is loaded")
