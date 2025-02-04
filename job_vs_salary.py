import pandas as pd
from collections import Counter
import json
df = pd.read_csv("job_listing_normalized_w_skills.csv")

my_dict = []
job_counter = Counter()


for index, row in df.iterrows():
    job_counter[row['Job Title']] += 1

        
top_10_job = dict(job_counter.most_common(10))

for job in top_10_job:
    job_df = df[df['Job Title'] == job]
    salary_ranges = job_df['Salary'].apply(lambda x: sum([float(num) for num in x.replace('$','').replace(',','').split('to')])/2)
    average= sum(salary_ranges)/len(salary_ranges)
    my_list = [f"{job}","%.2f" %average]
    my_dict.append(my_list)

json_obj = json.dumps(my_dict,indent = 1)
with open("JobvsSalary.json", "w") as outfile:
    outfile.write(json_obj)