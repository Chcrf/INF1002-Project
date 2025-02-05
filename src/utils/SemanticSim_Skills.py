import pickle
from transformers import AutoModel
from numpy.linalg import norm
import numpy as np
from pathlib import Path

class SemanticSim():
    '''
    A module that embeds Job Skills and compares it with a pre-embedded Job Skills for standardization 
    '''

    def __init__(self):
        '''
        Initializes the class with a transformers model that embeds string as well as a pre-embedded Job Skills file

        File Input:
            Fixed::src/utils/embeddings/skills_embedding.pkl
        '''
        self.model = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-small-en",trust_remote_code=True)
        self.skill_embeddings = list(pickle.load(open(Path(__file__).parent / "embeddings/skills_embedding.pkl","rb")))
    
    def encodeSkills(self, skills):
        '''
        Returns the embeddings of the skills

        Parameters:
            skills (list): List of skills to embed

        Returns:
            (list): List of skills along with its embeddings
        '''
        return zip(skills,self.model.encode(skills))

    def getSim(self, embeddings):
        '''
        Calculates the semantic similarity between the provided embeddings and skill_embeddings using Cosine Similarity

        Parameters:
            embeddings (list): The output of (Func) encodeSkills

        Returns:
            all_embeddings (list): A list of most confident predefined Job Skills along with the confidence score     
        '''
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

