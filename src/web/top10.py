import pandas as pd
import ast
from collections import Counter
import json

def createGraph1(df):
    '''
    Gets the skills column of the dataset, 
    Use counter to calculate the top 10 most common skills,
    Write the result to a JSON file
    '''
    df["skills"] = df["skills"].apply(lambda x: ast.literal_eval(x))
    my_dict = []
    skill_counter = Counter()

    for row in df["skills"]:
        for skill,confidence in row:
            
            if float(confidence)>=0.85:
                skill_counter[skill] += 1

            
    top_10_skills = skill_counter.most_common(10)


    for skill, count in top_10_skills:
        my_list = [skill,count]
        my_dict.append(my_list)

    json_obj = json.dumps(my_dict,indent = 1)
    with open("app/static/json/top10skills.json", "w") as outfile:
        outfile.write(json_obj)
