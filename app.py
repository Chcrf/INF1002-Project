from flask import Flask, render_template, request
from search import skills_search as search, load_dataset

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
df = load_dataset("job_listing_normalized_w_skills.csv")

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