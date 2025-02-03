import pandas as pd
import ast
import config.constants as CONSTANTS
from utils.SemanticSim_Occupation import SemanticSim as SemanticSim_Occupation
from utils.SemanticSim_Skills import SemanticSim as SemanticSim_Skills
from pathlib import Path

class DataNormalizer():
    def __init__(self):
        self.data =pd.read_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.SCRAPE_OUTPUT_FILE}",encoding="utf-8")

    def normalize(self):
        occupations = self.data["Job Title"].apply(lambda x: x.lower())
        skills = self.data["skills"].apply(lambda x: ast.literal_eval(x))


        semanticSim_occupation = SemanticSim_Occupation()
        semanticSim_skills = SemanticSim_Skills()

        embeddings = semanticSim_occupation.encodeOccupations(occupations)
        normalized_occupations_w_confidence = semanticSim_occupation.getSim(embeddings)
        normalized_occupations = [title.title().strip() for title,confidence in normalized_occupations_w_confidence]
        self.data['Job Title'] = normalized_occupations


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

        self.data["skills"] = normalized_skills

        self.data.to_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.SCRAPE_OUTPUT_FILE}",index=False)