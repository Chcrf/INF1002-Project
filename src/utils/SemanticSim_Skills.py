import pickle
from transformers import AutoModel
from numpy.linalg import norm
import numpy as np
from pathlib import Path

class SemanticSim():
    def __init__(self):
        self.model = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-small-en",trust_remote_code=True)
        self.skill_embeddings = list(pickle.load(open(Path(__file__).parent / "embeddings/skills_embedding.pkl","rb")))

    def cos_sim(self,a,b):
        return (a @ b.T) / (norm(a)*norm(b))
    
    def encodeSkills(self, skills):
        return zip(skills,self.model.encode(skills))

    def isAbbre(self,embeddings):
        similar_li = []
        for index in range(len(embeddings)):
            skill, embed = embeddings[index]
            for index2 in range(len(embeddings)):
                if(index == index2):
                    continue #Skip comparing itself
                skill2, embed2 = embeddings[index2]
                similarity = self.cos_sim(embed,embed2)
                if similarity > 0.9:
                    similar_li.append((skill,skill2))
                    # print(f"{skill} and {skill2} are similar",similarity)
        return similar_li

    def getSim(self, embeddings):
        # Extract skill names and their embeddings separately
        if(len(embeddings) == 0):
            return []
        skills, embed_arr = zip(*embeddings)  # Unpacking into lists
        skill_names, skill_embed_arr = zip(*self.skill_embeddings)

        # Convert to NumPy arrays
        embed_arr = np.array(embed_arr)  # (n, d)
        skill_embed_arr = np.array(skill_embed_arr)  # (m, d)

        # Compute cosine similarity in a vectorized way
        dot_products = embed_arr @ skill_embed_arr.T  # (n, m)
        norm_embed = norm(embed_arr, axis=1, keepdims=True)  # (n, 1)
        norm_skill_embed = norm(skill_embed_arr, axis=1)  # (m,)
        
        cos_sim_matrix = dot_products / (norm_embed * norm_skill_embed)  # (n, m)

        # Get the most similar skill for each embedding
        max_indices = np.argmax(cos_sim_matrix, axis=1)  # (n,)

        # Construct the result list
        all_embeddings = [(skill_names[i], cos_sim_matrix[j, i]) for j, i in enumerate(max_indices)]
        return all_embeddings

