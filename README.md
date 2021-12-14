# Chicago Crime

In this mini project, I take a look at crimes in Chicago as a whole and Hyde Park using pandas, plotly, and Google's BigQuery.

## How To Use the Jupyter Notebook
1. [Set up Python Client for Google BigQuery](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries).
2. Make sure you have the following packages: pandas, matplotlib, plotly, os, google.cloud
3. Replace credential_path with path to .json file produced in step 1.

## App Deployment
I also created a [web app](https://chicago-crime-dashboard.herokuapp.com/) with limited functionalities using Heroku. It took me quite some time to figure out how to integrate Heroku, Google 
Cloud and GitHub so that I can store all my code on GitHub. Found this [link](https://devdojo.com/bryanborge/adding-google-cloud-credentials-to-heroku)
that was super useful. Also, to deploy Heroku from GitHub, simply add the Procfile and setup.sh files in your repo, and add required packages in requirement.txt.


