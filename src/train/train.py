import subprocess
import sys
import spacy
from spacy.cli.train import train
from config import constants as CONSTANTS
from pathlib import Path
from preprocessing.dataCleaning import DataCleaning
from preprocessing.dataConverter import DataConverter
from preprocessing.gemini_AutoLabelling import GeminiAutoLabeller

class Trainer():
    '''
    A module that trains the NER model
    '''
    def __init__(self):
        '''
        Initializes the class and installs required spacy packages
        '''
        self._install_spacy_required_packages(CONSTANTS.MODE)

    def _install_spacy_required_packages(self,mode="CPU"):
        '''
        A private function that installs relevant spacy packages based on training mode

        Parameters:
            mode (str): Either GPU or CPU mode for training of model
        '''
        if(mode == "GPU"):
            package = "en_core_web_trf"
        else:
            package = "en_core_web_lg"
        
        if not spacy.util.is_package(package):
            subprocess.check_call([sys.executable, "-m", "spacy", "download", package])

    def train(self):
        '''
        Trains the NER model using the relevant training mode

        Training Mode Input:
            config/constants.py::MODE

        File Input:
            Fixed::datasets/training_data.spacy
            Fixed::datasets/valid_data.spacy
            Fixed::config/config_gpu.cfg
            Fixed::config/config_cpu.cfg
        
        File Output:
            Fixed::model (Directory)
        '''
        #1. Use gemini to auto label training data
        print("Performing Labelling...")
        autoLabeller = GeminiAutoLabeller()
        autoLabeller.autoLabel()
        #2. Clean gemini data
        print("Cleaning Data...")
        dataCleaner = DataCleaning()
        dataCleaner.dataReformatter()
        #3. Convert data to spacy processable
        print("Converting Data...")
        dataConverter = DataConverter()
        dataConverter.convert()

        training_data_path = str(Path(__file__).parent.parent/ "datasets/training_data.spacy")
        valid_data_path = str(Path(__file__).parent.parent/"datasets/valid_data.spacy")
        model_output_path = str(Path(__file__).parent.parent/"model")
        if CONSTANTS.MODE == "GPU":
            train(Path(__file__).parent.parent / "config/config_gpu.cfg",model_output_path,overrides={"paths.train": training_data_path, "paths.dev": valid_data_path})
        else: # Default mode -> CPU
            train(Path(__file__).parent.parent / "config/config_cpu.cfg",model_output_path,overrides={"paths.train": training_data_path, "paths.dev": valid_data_path})
