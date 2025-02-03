import pickle
import numpy as np
from transformers import AutoModel
from numpy.linalg import norm
from pathlib import Path

class SemanticSim():
    def __init__(self):
        self.model = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-small-en",trust_remote_code=True)
        self.occupation_embeddings = list(pickle.load(open(Path(__file__).parent / "embeddings/occupations_embedding.pkl","rb")))

    def cos_sim(self,a,b):
        return (a @ b.T) / (norm(a)*norm(b))
    
    def encodeOccupations(self, occupation):
        return list(zip(occupation,self.model.encode(occupation)))

    def getSim(self,embeddings):

        if(len(embeddings) == 0):
            return []
        occupations, embed_arr = zip(*embeddings)  # Unpacking into lists
        occupation_name, occupation_embed_arr = zip(*self.occupation_embeddings)

        # Convert to NumPy arrays
        embed_arr = np.array(embed_arr)  # (n, d)
        occupation_embed_arr = np.array(occupation_embed_arr)  # (m, d)

        # Compute cosine similarity in a vectorized way
        dot_products = embed_arr @ occupation_embed_arr.T  # (n, m)
        norm_embed = norm(embed_arr, axis=1, keepdims=True)  # (n, 1)
        norm_occupation_arr = norm(occupation_embed_arr, axis=1)  # (m,)
        
        cos_sim_matrix = dot_products / (norm_embed * norm_occupation_arr)  # (n, m)

        # Get the most similar skill for each embedding
        max_indices = np.argmax(cos_sim_matrix, axis=1)  # (n,)

        all_embeddings = [(occupation_name[i], cos_sim_matrix[j, i]) for j, i in enumerate(max_indices)]
        return all_embeddings

