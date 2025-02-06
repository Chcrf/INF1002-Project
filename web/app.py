from flask import Flask, render_template, request
import pandas as pd

from search import skills_search as search, load_dataset

from top10 import createGraph1
from pie import createGraph2
from job_vs_salary import createGraph3

app = Flask(__name__,
            static_url_path='', 
            static_folder='app/static',
            template_folder='app/templates')

# Load datasets for creating graph and search functions
df2 = pd.read_csv("job_listing_normalized_w_skills.csv")
df = load_dataset("job_listing_normalized_w_skills.csv")

# Create graph jsons
createGraph1(df2)
createGraph2(df2)
createGraph3(df2)

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "POST":
        # Error Handling: 0 = No error, 1 = Invalid input, 2 = No matched
        jobRole = request.form['searching']
        try:
            core, additional, err = search(df, jobRole)
            if additional:
                if type(additional) is list:
                    additional_list = True
                else:
                    additional_list = False
    
            return render_template('index.html',
                                    searched_job = jobRole,
                                    core_skills = core,
                                    additional_check = additional_list,
                                    additional_skills = additional,
                                    error = err)
        except Exception as e:
            print("An error occurred while searching for skills: ", e)
            return render_template('index.html')
    
    return render_template('index.html')

if __name__ == '__main__':
   app.run()