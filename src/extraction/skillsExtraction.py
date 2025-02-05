import spacy
import re
import pandas as pd
import config.constants as CONSTANTS
from pathlib import Path
from tqdm import tqdm 
from utils.DataCleaner import DataCleaner

class SkillExtractor():
    '''
    A module that extracts skills from SCRAPE_OUTPUT_FILE
    '''
    def __init__(self):
        '''
        Initializes the class with DataCleaner
        '''
        self.dataCleaner = DataCleaner()

    def extract_skills(self):
        '''
        Preprocesses SCRAPE_OUTPUT_FILE, extract skills and store it in SCRAPE_OUTPUT_FILE  

        Model Input:
            Fixed::src/model/model-best

        File Input:
            config/constants.py::SCRAPE_OUTPUT_FILE

        File Output:
            config/constants.py::SCRAPE_OUTPUT_FILE
        '''
        data = pd.read_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.SCRAPE_OUTPUT_FILE}")
        dataCleaner = self.dataCleaner
        nlp = spacy.load(str(Path(__file__).parent.parent / f"model/model-best"))
        extracted_skills = []
        for jd in tqdm(list(data["Job Description"])):
            jd = dataCleaner.newline_remover(jd)
            sents = [str(sent) for sent in dataCleaner.sentencize(jd)]
            skills = set()
            nlp_output = nlp.pipe(sents)
            for doc in nlp_output:
                for ent in doc.ents:
                    skills.add(str(ent).lower())

            extracted_skills.append(list(skills))
        data = data.assign(skills=extracted_skills)
        data.to_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.SCRAPE_OUTPUT_FILE}",index=False)
