import pandas as pd
from collections import Counter
import json
df = pd.read_csv("job_listing_normalized_w_skills.csv")
my_list = []

category_counter = Counter()


for index, row in df.iterrows():
    category_counter[row['Categorie']] += 1

        
top_15_category = category_counter.most_common(15)
for skill, count in top_15_category:
    my_dict = {}
    my_dict['name'] = skill
    my_dict['value'] = count
    my_list.append(my_dict)
print(my_list)
json_obj = json.dumps(my_list,indent = 1)
with open("pie.json", "w") as outfile:
    outfile.write(json_obj)
