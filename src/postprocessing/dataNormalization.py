import pandas as pd
import ast
import config.constants as CONSTANTS
from utils.SemanticSim_Occupation import SemanticSim as SemanticSim_Occupation
from utils.SemanticSim_Skills import SemanticSim as SemanticSim_Skills
from pathlib import Path

class DataNormalizer():
    '''
    A module that converts Job Title and Skills to a standardized format by using semantic similarity.
    '''
    def normalize(self):
        '''
        Standardizes Job Title and Skills using semantic similarity

        File Input:
            config/constants.py::SCRAPE_OUTPUT_FILE
        
        File Output:
            config/constants.py::SCRAPE_OUTPUT_FILE
        '''
        data =pd.read_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.SCRAPE_OUTPUT_FILE}",encoding="utf-8")
        occupations = data["Job Title"].apply(lambda x: x.lower())
        skills = data["skills"].apply(lambda x: ast.literal_eval(x))

        semanticSim_occupation = SemanticSim_Occupation()
        semanticSim_skills = SemanticSim_Skills()

        embeddings = semanticSim_occupation.encodeOccupations(occupations)
        normalized_occupations_w_confidence = semanticSim_occupation.getSim(embeddings)
        normalized_occupations = [title.title().strip() for title,confidence in normalized_occupations_w_confidence]
        data['Job Title'] = normalized_occupations


        normalized_skills = []
        collated_skills = set()

        for row in skills:
            row = set(row)
            collated_skills.update(row)

        embeddings = dict(semanticSim_skills.encodeSkills(list(collated_skills)))

        for row in skills:
            row = set(row)
            embedding = [(skill,embeddings[skill]) for skill in row]
            all_most_similar = semanticSim_skills.getSim(embedding)
            normalized_skills.append(all_most_similar)

        data["skills"] = normalized_skills

        data.to_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.SCRAPE_OUTPUT_FILE}",index=False)