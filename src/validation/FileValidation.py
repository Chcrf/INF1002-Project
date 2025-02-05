from config import constants as CONSTANTS
from pathlib import Path
import pandas as pd
import spacy

class FileValidation():
    '''
    A module that performs validation of files before training or processing of data
    '''
    def checkTrainFile(self):
        '''
        Checks if training data exists and is properly formatted
        '''
        GEMINI_INPUT_FILE = Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_INPUT_FILE}"

        if not GEMINI_INPUT_FILE.exists():
            return (False, f"Please create the file {str(GEMINI_INPUT_FILE)}")
        gemini_input_file = pd.read_csv(GEMINI_INPUT_FILE)
        
        if "job_description" not in gemini_input_file: # Check if column exists
            return (False, f"Please have a 'job_description' column in {str(GEMINI_INPUT_FILE)}")
        if len(gemini_input_file) == 0:
            return (False, f"Please have some data in {str(GEMINI_INPUT_FILE)}")
    
        return (True,None)
        
    def checkProcessFile(self):
        '''
        Checks if data to process exists and is properly formatted as well as the existence of the model
        '''
        SCRAPE_OUTPUT_FILE = Path(__file__).parent.parent / f"datasets/{CONSTANTS.SCRAPE_OUTPUT_FILE}"
        OCCUPATION_EMBEDDINGS = Path(__file__).parent.parent/f"utils/embeddings/occupations_embedding.pkl"
        SKILLS_EMBEDDINGS = Path(__file__).parent.parent/f"utils/embeddings/skills_embedding.pkl"
        if not (SCRAPE_OUTPUT_FILE).exists():
            return (False, f"Please create the file {SCRAPE_OUTPUT_FILE}")
        data = pd.read_csv(SCRAPE_OUTPUT_FILE)
        if "Job Description" not in data: # Check if column exists
            return (False, f"Please have a 'Job Description' column in {str(SCRAPE_OUTPUT_FILE)}")
        if "Job Title" not in data: # Check if column exists
            return (False, f"Please have a 'Job Title' column in {str(SCRAPE_OUTPUT_FILE)}")
        if len(data) == 0:
            return (False, f"Please have some data in {str(SCRAPE_OUTPUT_FILE)}")
        try:
            spacy.load(str(Path(__file__).parent.parent / f"model/model-best"))
        except:
            return (False, f"Please have a model at {str(Path(__file__).parent.parent)/'/model/model-best'}")
        if not (OCCUPATION_EMBEDDINGS).exists():
            return (False, f"Please create the file {str(OCCUPATION_EMBEDDINGS)}")
        if not (SKILLS_EMBEDDINGS).exists():
            return (False, f"Please create the file {str(SKILLS_EMBEDDINGS)}")
        return (True,None)