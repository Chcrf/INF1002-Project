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
    def __init__(self):
        self.install_spacy_required_packages(CONSTANTS.MODE)

    def install_spacy_required_packages(self,mode="CPU"):
        if(mode == "GPU"):
            package = "en_core_web_trf"
        else:
            package = "en_core_web_lg"
        
        if not spacy.util.is_package(package):
            subprocess.check_call([sys.executable, "-m", "spacy", "download", package])

    def train(self):
        #1. Use gemini to auto label training data
        autoLabeller = GeminiAutoLabeller()
        autoLabeller.autoLabel()
        #2. Clean gemini data
        dataCleaner = DataCleaning()
        dataCleaner.dataReformatter()
        #3. Convert data to spacy processable
        dataConverter = DataConverter()
        dataConverter.convert()

        training_data_path = str(Path(__file__).parent.parent/ "datasets/training_data.spacy")
        valid_data_path = str(Path(__file__).parent.parent/"datasets/valid_data.spacy")
        model_output_path = str(Path(__file__).parent.parent/"model")
        if CONSTANTS.MODE == "GPU":
            train(Path(__file__).parent.parent / "config/config_gpu.cfg",model_output_path,overrides={"paths.train": training_data_path, "paths.dev": valid_data_path})
        else: # Default mode -> CPU
            train(Path(__file__).parent.parent / "config/config_cpu.cfg",model_output_path,overrides={"paths.train": training_data_path, "paths.dev": valid_data_path})
