import os
from pathlib import Path 
import pandas as pd
from fuzzywuzzy import process
import ast


# Load dataset
def load_dataset(filename):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_csv(Path(current_dir) / filename) 
        return df
    except FileNotFoundError:
        print("Error: The dataset file was not found.")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The dataset file is empty.")
        raise
    except Exception as e:
        print("An unexpected error occurred while loading the dataset: ", e)
        raise

def find_similar_job(user_input, jobs):
    """Fuzzy match to find the closest job title using Levenshtein distance"""
    try:
        match = process.extractOne(user_input, jobs)
        if match:
            return match[0] 
        else: None
    except Exception as e:
        print("An error occurred while finding a similar job: ", e)

def get_high_confidence_skills(skills_str, threshold=0.85):
    """Extracts the job skills for the given job title and if the confidence level is above the threshold"""
    try:
        skills_list = ast.literal_eval(skills_str)
        return {skill for skill, score in skills_list if score >= threshold}
    except (ValueError, SyntaxError) as e:
        print("An error occurred while parsing skills: ", e)

def get_common_skills_for_title(df, target_title, threshold=0.85):
    """Compares the skills with other similar job titles, outputs only skills that all the compared jobs have into a list known as common_skills. """
    # Get all jobs with same title
    try:
        same_title_jobs = df[df['Job Title'] == target_title]
        
        if len(same_title_jobs) < 1:
            return set()
        
        # Get skills for all same-title jobs
        skill_sets = []
        for _, row in same_title_jobs.iterrows():
            skill_sets.append(get_high_confidence_skills(row['skills'], threshold))
        
        # Find intersection across all same-title jobs
        common_skills = set.intersection(*skill_sets) if skill_sets else set()
        return common_skills
    except Exception as e:
        print("An error occurred while getting common skills: ", e)

def skills_search(df, job):
    """User interaction flow"""
    try:
        user_input = job.strip()
        all_jobs = df['Job Title'].unique().tolist()
        
        matched_title = find_similar_job(user_input, all_jobs)
        if not matched_title:
            print("No matching job found.")
            return _, _, 2
        
        common_skills = get_common_skills_for_title(df, matched_title)
        
        # Get individual job skills (for single-entry case)
        individual_skills = set()
        for _, row in df[df['Job Title'] == matched_title].iterrows():
            individual_skills.update(get_high_confidence_skills(row['skills']))
        
        # Display results
        print(f"\nAnalysis for: '{matched_title}'")
        print("--------------------------------")
        
        if common_skills:
            print(f"Core skills common to ALL '{matched_title}' roles:")
            for idx, skill in enumerate(sorted(common_skills), 1):
                print(f"{idx}. {skill}")
                # return common_skills
            
            if len(common_skills) < len(individual_skills):
                print("\nAdditional skills from individual postings:")
                additional = sorted(individual_skills - common_skills)
                for idx, skill in enumerate(additional, 1):
                    print(f"{idx}. {skill}")
                return common_skills, additional, 0
            return common_skills, _, 0
        else:
            print(f"Key skills for '{matched_title}':")
            for idx, skill in enumerate(sorted(individual_skills), 1):
                print(f"{idx}. {skill}")
            return individual_skills, _, 0
    except Exception as e:
        print("An error occurred during the skills search: ", e)
        return _, _, 1

if __name__ == '__main__':
    df = load_dataset("job_listing_normalized_w_skills.csv")
    skills_search(df)