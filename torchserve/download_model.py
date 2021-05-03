import transformers
from pathlib import Path
import os
import json
import torch
from sentence_transformers import SentenceTransformer


print(f'PyTorch version: {torch.__version__}')

NEW_DIR = "./sentence_model"
try:
  os.mkdir(NEW_DIR)
except OSError:
  print ("Creation of directory %s failed" % NEW_DIR)


xformer = SentenceTransformer('stsb-roberta-base')
xformer.save(NEW_DIR)
print("model is saved")

loaded_xformer = SentenceTransformer(NEW_DIR)
print("model is loaded")
