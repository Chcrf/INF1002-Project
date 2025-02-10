from flask import Flask, render_template, request
from werkzeug.serving import run_simple
import pandas
from config import constants as CONSTANTS
from pathlib import Path
import logging
import sys

from .search import skills_search as search, load_dataset

from .top10 import createGraph1
from .pie import createGraph2
from .job_vs_salary import createGraph3

class RunWeb():
    '''
    A module that starts up a web server
    '''
    def __init__(self):
        '''
        Creates app object which serves as a central registry for the view functions, URL rules, template configurations and more.
        
        As well as reading the csv file required for data visualisation
        '''
        self.app = Flask(__name__,
                         static_url_path='', 
                         static_folder='app/static',
                         template_folder='app/templates')
        try:
            self.df = pandas.read_csv(Path(__file__).parent.parent / f"datasets/Out-of-the-box/{CONSTANTS.DATA_VISUALISATION_INPUT_FILE}")
        except FileNotFoundError:
            print("\n⛔ Error: The dataset file was not found. \n💡 Solution: Download and extract the prepared datasets, and place them in the src/ directory as shown in the README.\n")
            raise

    def _createGraphs(self):
        '''
        A private function for generating JSON outputs for data visualisation on the websites
        '''

        createGraph1(self.df)
        createGraph2(self.df)
        createGraph3(self.df)
        
    def _add_endpoint(self, URL, endpointName, handler, requestMethods):
        '''
        A private function to connect a URL rule

        Parameters:
            endpoint (str): URL string
            endpointName (str): The endpoint string for the registered URL associating to the view function
            handler (func): The function handling the requests
            requestMethods (list): List of methods the URL is limited to
        '''
        self.app.add_url_rule(URL, endpointName, handler, methods=requestMethods)

    def home(self):
        '''
        Creates a handler for requests from web server under a specific endpoint
        '''

        if request.method == "POST":
            # Error Handling: 0 = No error, 1 = Invalid input, 2 = No matched
            jobRole = request.form['searching']

            if jobRole == "":
                return render_template('index.html')

            try:
                matched_title, core, additional, err = search(self.df, jobRole)
                
                if type(additional) is list:
                    additional_list = True
                else:
                    additional_list = False
        
                return render_template('index.html',
                                        searched_job = jobRole.upper(),
                                        matched_title = matched_title.upper(),
                                        core_skills = core,
                                        additional_check = additional_list,
                                        additional_skills = additional,
                                        error = err)
            except Exception as e:
                print("An error occurred while searching for skills: ", e)
                return render_template('index.html')
        
        return render_template('index.html')   

    def startWeb(self):
        '''
        Starts the webserver on localhost:8080
        '''
        self._createGraphs()
        self._add_endpoint('/', 'home', self.home ,['GET', 'POST'])
        log = logging.getLogger('werkzeug')
        log.disabled = True
        print(f"* Running on http://127.0.0.1:8080\nPress CTRL+C to quit", file=sys.stderr) # sys.stderr to match Flask’s default output behavior
        run_simple('127.0.0.1', 8080, self.app)