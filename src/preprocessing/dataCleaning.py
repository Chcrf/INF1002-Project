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
    '''
    A module that cleans the annotated dataset from Google Gemini output
    '''

    def __init__(self):
        '''
        Initializes the class with DataCleaner
        '''
        self.dataCleaner = DataCleaner()

    def _extract_skills(self, skill,skill_li):
        '''
        A private function for extracting skills from Google Gemini JSON output

        Parameters:
            skill (dict): A dictionary that contains a skill 
            skill_li (list): A shared list that will store the extracted skill  
        '''
        if "text" in skill:
            skill_li.append(skill["text"].title())
        elif "entity" in skill:
            skill_li.append(skill["entity"].title())

    def dataReformatter(self):
        '''
        Reformats the extracted Google Gemini JSON output and converts the Job Description to a standardized format for training

        File Input:
            config/constants.py::GEMINI_OUTPUT_FILE
        
        File Output:
            config/constants.py::GEMINI_OUTPUT_FILE
        '''
        self.data = pd.read_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_OUTPUT_FILE}")
        self.data["job_skills"] = self.data["job_skills"].apply(lambda x: str(x).replace("```json","").replace("```","").strip())
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
                        self._extract_skills(ent_skill,job_skills_list)
                else:
                    self._extract_skills(skill,job_skills_list)
            job_description = dataCleaner.newline_remover(row["job_description"])
            new_df_dict["job_description"].append(job_description)
            new_df_dict["job_skills"].append(job_skills_list)

        pd.DataFrame(new_df_dict).to_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_OUTPUT_FILE}")
    


