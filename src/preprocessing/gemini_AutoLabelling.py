'''
Uses Google Gemini for autolabelling
Input file: job_desc.csv
Output file: job_desc_with_skills.csv
'''

import google.generativeai as genai
import pandas
import time
from tqdm import tqdm
from config import constants as CONSTANTS
from pathlib import Path

class GeminiAutoLabeller():
    def __init__(self):
        genai.configure(api_key=CONSTANTS.API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        self.prompt='''
        1.You are a Named Entity Recognition
        2.Do some analysis to extract the Entity from the text for technical and soft skills.
        3.Output skills category as SKI
        4.Return this result as JSON for each entity with character offset from each result.
        Analyze the sentences as follow: "'
        '''

        self.job_desc = pandas.read_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_INPUT_FILE}")
        self.job_desc_with_skills = pandas.DataFrame(columns=["job_description","job_skills"])

    def autoLabel(self):
        #Gemini 1.5 flash can only accept 15 requests per minute
        start_time = time.time()
        count = 0
        for index, row in tqdm(self.job_desc.iterrows(), total=self.job_desc.shape[0]):
            count+=1
            job_description = row["job_description"]
            Response = self.model.generate_content(self.prompt+job_description+'"').text
            self.job_desc_with_skills.loc[-1]=[job_description,Response]
            self.job_desc_with_skills.index = self.job_desc_with_skills.index + 1
            if time.time()-start_time < 60 and count >=15:
                time.sleep(61-time.time()-start_time) # Wait for a few seconds until the request limit resets. 61 acts as a fail-safe
                start_time = time.time()  
                count=0

        self.job_desc_with_skills.to_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_OUTPUT_FILE}")