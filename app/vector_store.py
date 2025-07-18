import faiss
import numpy as np
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata: List[Dict[str, Any]] = []

    def add(self, embeddings: List[np.ndarray], metadata: List[Dict[str, Any]]) -> None:
        self.index.add(np.array(embeddings))
        self.metadata.extend(metadata)

    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[Dict[str, Any]]:
        D, I = self.index.search(np.array([query_embedding]), k)
        return [self.metadata[i] for i in I[0]]