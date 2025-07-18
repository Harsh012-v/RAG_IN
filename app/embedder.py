from sentence_transformers import SentenceTransformer
from typing import List, Union
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_texts(texts: List[str]) -> torch.Tensor:
    return model.encode(texts, convert_to_tensor=True)