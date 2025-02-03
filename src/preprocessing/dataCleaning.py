'''
Code to clean Google Gemini output
Input file: job_desc_with_skills.csv
Output file: job_desc_with_skills.csv
'''

import pandas as pd
import json
from pathlib import Path
from config import constants as CONSTANTS
from utils.DataCleaner import DataCleaner

class DataCleaning():
    def __init__(self):
        self.dataCleaner = DataCleaner()
    
        self.data = pd.read_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_OUTPUT_FILE}")
        self.data["job_skills"] = self.data["job_skills"].apply(lambda x: str(x).replace("```json","").replace("```","").strip())

    def extract_skills(self, skill,skill_li):
        if "text" in skill:
            skill_li.append(skill["text"].title())
        elif "entity" in skill:
            skill_li.append(skill["entity"].title())

    def labeller(self, sentence, job_skills):
        skill_li = []
        for skill in job_skills:
            if skill.lower() in sentence.lower():
                skill_li.append(skill)
        return skill_li

    def dataReformatter(self):
        data = self.data
        dataCleaner = self.dataCleaner
        new_df_dict = {
        "job_description":[],
        "job_skills":[]

        }
        for index, row in data.iterrows():
            job_skills = json.loads(row["job_skills"])
            job_skills_list = []
            for skill in job_skills:
                if "entities" == skill:
                    for ent_skill in job_skills["entities"]:
                        self.extract_skills(ent_skill,job_skills_list)
                else:
                    self.extract_skills(skill,job_skills_list)
            job_description = dataCleaner.newline_remover(row["job_description"])
            new_df_dict["job_description"].append(job_description)
            new_df_dict["job_skills"].append(job_skills_list)

        pd.DataFrame(new_df_dict).to_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_OUTPUT_FILE}")
    


