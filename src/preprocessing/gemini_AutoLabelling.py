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
    '''
    A module that relies on Google Gemini for autolabelling of dataset for model training
    '''

    def __init__(self):
        '''
        Initializes Google Gemini 1.5 Flash using an API Key as well as declaring the prompt to use

        API Key Input:
            config/constants.py::API_KEY
        '''
        genai.configure(api_key=CONSTANTS.API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        self.prompt='''
        1.You are a Named Entity Recognition
        2.Do some analysis to extract the Entity from the text for technical and soft skills.
        3.Output skills category as SKI
        4.Return this result as JSON for each entity with character offset from each result.
        Analyze the sentences as follow: "'
        '''

    def autoLabel(self):
        '''
        Prompts the Google Gemini 1.5 Flash to label the Job Description with its relevant skills

        File Input:
            config/constants.py::GEMINI_INPUT_FILE

        File Output:
            config/constants.py::GEMINI_OUTPUT_FILE
        '''
        job_desc = pandas.read_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_INPUT_FILE}")
        job_desc_with_skills = pandas.DataFrame(columns=["job_description","job_skills"])

        #Gemini 1.5 flash can only accept 15 requests per minute
        start_time = time.time()
        count = 0
        for index, row in tqdm(job_desc.iterrows(), total=job_desc.shape[0]):
            count+=1
            job_description = row["job_description"]
            Response = self.model.generate_content(self.prompt+job_description+'"').text
            job_desc_with_skills.loc[-1]=[job_description,Response]
            job_desc_with_skills.index = job_desc_with_skills.index + 1
            if time.time()-start_time < 60 and count >=15: # When request limit reaches
                time.sleep(61-time.time()-start_time) # Wait for a few seconds until the request limit resets. 61 acts as a fail-safe
                start_time = time.time()  
                count=0
            elif time.time()-start_time > 60: # When request limit did not reach, reset the time and count
                start_time = time.time()  
                count=0

        job_desc_with_skills.to_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_OUTPUT_FILE}")