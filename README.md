# Chicago-Crime

In this mini project, I take a look at crimes in Chicago as a whole and Hyde Park (where the University of Chicago is) in particular from 2015 to 2020 using pandas, plotly, and Google's BigQuery. For the final analysis, see my blog post: https://hvohub.wordpress.com/2021/07/18/a-look-at-crime-in-chicago-and-hyde-park/. For how the code works, I've put comments in the jupyter notebook.

## How To Use the Jupyter Notebook
1. [Set up Python Client for Google BigQuery](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries) (The dataset is large enough to give pandas trouble, so I have to use BigQuery SQL)
2. Make sure you have the following packages: pandas, matplotlib, plotly, os, google.cloud
3. Replace credential_path with path to .json file produced in step 1.
