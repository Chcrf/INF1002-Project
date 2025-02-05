import spacy
import re

class DataCleaner():
    '''
    A module the provides data cleaning functions
    '''
    def __init__(self):
        '''
        Initializes the class with spacy pretrained model
        '''
        self.sentencizer=spacy.blank('en')
        self.sentencizer.add_pipe("sentencizer")
        
    def newline_remover(self,text):
        '''
        Returns provided string with repeated spaces and newline removed

        Parameters:
            text (str): The string to remove repeated spaces and newline from

        Returns:
            (str): The string without newline and repeated spaces
        '''
        return re.sub('\s{2,}', ' ', text.replace("\n"," "))

    def sentencize(self,text):
        '''
        Returns provided string as sentences

        Parameters:
            text (str): The string to convert to sentences

        Returns:
            (list): List of sentences
        '''
        return list(self.sentencizer(text).sents)
