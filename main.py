import sys
from src.validation.FileValidation import FileValidation
from src.train.train import Trainer
from src.scrape.scrape import Scraper
from src.extraction.skillsExtraction import SkillExtractor  
from src.postprocessing.dataNormalization import DataNormalizer

class Main():
    '''
    The main module allows users to run different command for the program
    '''
    def __init__(self):
        '''
        Initializes FileValidation for performing validation on files.
        '''
        self.fileValidation = FileValidation()
    
    def commands(self):
        '''
        Calls the relevant function of the program

        Usage: python main.py <Mode>

        Mode:
            Train: Perform model training
            Scrape: Perform scraping on MyCareersFuture
            Process: Use the trained model
        '''
        if(len(sys.argv) < 2 or sys.argv[1] not in ["train","scrape","process"]):
            print("Enter either Train, Scrape, or Process")
            return
        mode = sys.argv[1].lower()
        try:
            if(mode == "train"):
                (success, msg) = self.fileValidation.checkTrainFile()
                if(not success):
                    raise Exception(msg)
                print("🏋 Training...")
                trainer = Trainer()
                trainer.train()
                print("="*20)
                print("✅ Job Completed")
            elif(mode == "scrape"):
                print("⛏️ Scraping...")
                scraper = Scraper()
                scraper.scrape()
                print("="*20)
                print("✅ Job Completed")
            elif(mode == "process"):
                (success, msg) = self.fileValidation.checkProcessFile()
                if(not success):
                    raise Exception(msg)
                print("🧠 Processing...")
                extractor = SkillExtractor()
                extractor.extract_skills()
                normalizer = DataNormalizer()
                normalizer.normalize()
                print("="*20)
                print("✅ Job Completed")
        except Exception as ex:
            print("🚨 Oops Something Happened")
            print(repr(ex))

if __name__ == "__main__":
    main = Main()
    main.commands()