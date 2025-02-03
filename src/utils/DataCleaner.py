import spacy
import re

class DataCleaner():
    def __init__(self):
        self.sentencizer=spacy.blank('en')
        self.sentencizer.add_pipe("sentencizer")
        
    def newline_remover(self,text):
        return re.sub('\s{2,}', ' ', text.replace("\n"," "))

    def sentencize(self,text):
        return list(self.sentencizer(text).sents)
