import sys

def commands():
    if(len(sys.argv) < 2 or sys.argv[1] not in ["train","scrape","process"]):
        print("Enter either Train, Scrape, or Process")
        return
    mode = sys.argv[1].lower()
    try:
        if(mode == "train"):
            from src.train.train import Trainer
            print("🏋 Training...")
            trainer = Trainer()
            trainer.train()
            print("="*20)
            print("✅ Job Completed")
        elif(mode == "scrape"):
            from src.scrape.scrape import Scraper
            print("⛏️ Scraping...")
            scraper = Scraper()
            scraper.scrape()
            print("="*20)
            print("✅ Job Completed")
        elif(mode == "process"):
            from src.extraction.skillsExtraction import SkillExtractor  
            from src.postprocessing.dataNormalization import DataNormalizer
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
    commands()