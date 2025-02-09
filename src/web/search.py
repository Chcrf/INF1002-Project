import os
from pathlib import Path 
import pandas as pd
from fuzzywuzzy import process
import ast


def load_dataset(filename):
    """
    Loads job listing as a pandas dataframe.
    
    Args:
        filename (str): The name of the CSV file containing the job listings.

    Returns:
        df (pd.DataFrame): A DataFrame containing the job listings.

    Raises:
        FileNotFoundError: If the specified file is not found.
        pd.errors.EmptyDataError: If the specified file is empty.
        Exception: If an unexpected error occurs while loading the dataset.
    """
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
    """ 
    Fuzzy match to find the closest job title to the user input.
    
    Args:
        user_input (str): The job title input by the user.
        jobs (list): A list of job titles to search from.

    Returns:
        match (str): The closest matching job title if a match is found (using a threshold score of 80 Levenshtein distance), otherwise None.

    Raises:
        Exception: If an error occurs while finding a similar job.
    """
    try:
        match = process.extractOne(user_input, jobs, score_cutoff=80)
        if match:
            return match[0] 
        else: None
    except Exception as e:
        print("An error occurred while finding a similar job: ", e)

def get_high_confidence_skills(skills_str, threshold=0.85):
    """
    Extracts the job skills based on confidence rating threshold
    
    Args:
        skills_str (str): A string representation of a list of tuples, where each tuple contains a skill and its confidence score.
        threshold (float): The confidence threshold for filtering skills.

    Returns:
        high_skills (set): A set of skills that meet or exceed the confidence threshold.

    Raises:
        ValueError, SyntaxError: If an error occurs while parsing the skills string.
    """
    try:
        if isinstance(skills_str, list):
            skills_list = skills_str
        else:
            skills_list = ast.literal_eval(skills_str)


        high_skills = set()
        for skill, score in skills_list:
            if score >= threshold:
                high_skills.add(skill)
            else: continue

        return high_skills
    except (ValueError, SyntaxError) as e:
        print("An error occurred while parsing skills: ", e)

def common_skills_by_title(df, target_title, threshold=0.85):
    """
    Filters out common skills for all jobs listings with a similar job title.

    Args:
        target_title (str): The job title to search for.
        threshold (float): The confidence threshold for filtering skills.

    Returns:
        common_skills (set): A set of skills common to all job listings with the same title.

    Raises:
        Exception: If an error occurs while getting common skills.
    """
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
    """
    User interaction flow

    Args:
        df (pd.DataFrame): The DataFrame containing job listings.

    Raises:
        Exception: If an error occurs during the skills search.
    """
    try:
        user_input = job.strip()
        all_jobs = df['Job Title'].unique().tolist()
        
        matched_title = find_similar_job(user_input, all_jobs)
        if not matched_title:
            print("No matching job found.")
            return 0, 0, 0, 2
        
        common_skills = common_skills_by_title(df, matched_title)
        
        # Get individual job skills (for single-entry case)
        individual_skills = set()
        for _, row in df[df['Job Title'] == matched_title].iterrows():
            individual_skills.update(get_high_confidence_skills(row['skills']))
        
        if common_skills:
            if len(common_skills) < len(individual_skills):
                additional = sorted(individual_skills - common_skills)
                return matched_title, common_skills, additional, 0
            return matched_title, common_skills, 0, 0
        else:
            return matched_title, individual_skills, 0, 0
    except Exception as e:
        print("An error occurred during the skills search: ", e)
        return 0, 0, 0, 1
