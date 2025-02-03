import pandas as pd
import spacy
import ast
from pathlib import Path
from tqdm import tqdm
from spacy.matcher import PhraseMatcher
from spacy.tokens import DocBin, Span
from spacy.util import filter_spans
from sklearn.model_selection import train_test_split
from config import constants as CONSTANTS
from utils.DataCleaner import DataCleaner

class DataConverter():
    def __init__(self):
        self.dataCleaner = DataCleaner()
        self.data = pd.read_csv(Path(__file__).parent.parent / f"datasets/{CONSTANTS.GEMINI_OUTPUT_FILE}")
        self.nlp=spacy.blank('en')        
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        
    def labeller(self, sentence, job_skills):
        skill_li = []
        for skill in job_skills:
            if skill.lower() in sentence.lower():
                skill_li.append(skill)
        return skill_li    
    
    def create_dataset(self, text, filename):
        LABEL = "SKILL"
        doc_bin = DocBin()  # create a DocBin object

        for index,row in tqdm(text.iterrows()):
            doc = self.nlp.make_doc(row["job_description"])
            ents = []

            for match_id, start, end in self.matcher(doc):
                span = Span(doc,start, end, label=LABEL)
                if span is None or span.text.isspace():
                    print("Skipping entity")
                else:
                    ents.append(span)
            filtered_ents = filter_spans(ents)
            doc.ents = filtered_ents
            doc_bin.add(doc)
        doc_bin.to_disk(filename)

    def convert(self):
        new_df_dict = {
            "job_description":[],
            "job_skills":[]

        }
        skill_set = set()
        for index, row in self.data.iterrows():
            job_skills = [skill.strip() for skill in ast.literal_eval(row["job_skills"])] #Remove invalid whitespaces
            job_description = row["job_description"]
            sentencize_job_desc = self.dataCleaner.sentencize(job_description)
            for sentence in sentencize_job_desc:
                sentence = str(sentence).lower()
                sent_skill_li = self.labeller(sentence, job_skills)
                new_df_dict["job_description"].append(sentence)
                new_df_dict["job_skills"].append(sent_skill_li)
            for skill in job_skills:
                skill_set.add(skill)

        patterns = [self.nlp.make_doc(skill) for skill in skill_set]
        self.matcher.add("SKILL",patterns)

        new_df = pd.DataFrame(new_df_dict)
        x_train, x_test = train_test_split(new_df,test_size=0.3)
        self.create_dataset(x_train, Path(__file__).parent.parent / "datasets/training_data.spacy")
        self.create_dataset(x_test, Path(__file__).parent.parent / "datasets/valid_data.spacy")  


