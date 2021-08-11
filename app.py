import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.cloud import bigquery
import os

# Tell Google API where the credentials are
credential_path = '../Credentials/chicago-crime-319621-bb3dcff247ca.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
client = bigquery.Client()

st.title('Chicago Crime')

sql_chicago = """select primary_type, count(primary_type) as count
                from `bigquery-public-data.chicago_crime.crime` 
                where date between '2015-01-01' and '2020-12-31' and domestic = False
                group by 1;"""

sql_hp = """select primary_type, count(primary_type) as count
                from `bigquery-public-data.chicago_crime.crime` 
                where date between '2015-01-01' and '2020-12-31' and community_area = 41 and domestic = False
                group by 1;"""

chicago = client.query(sql_chicago).to_dataframe()
hyde_park = client.query(sql_hp).to_dataframe()

# Group crimes that are are
chicago.loc[chicago['count'] < float(chicago.quantile(0.6)), 'primary_type'] = 'OTHER OFFENSE'
hyde_park.loc[hyde_park['count'] < float(hyde_park.quantile(0.6)), 'primary_type'] = 'OTHER OFFENSE'

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=chicago['primary_type'], values=chicago['count'], name=""), 1, 1)
fig.add_trace(go.Pie(labels=hyde_park['primary_type'], values=hyde_park['count'], name=""), 1, 2)

# Use `hole` to create a donut-like pie chart
#fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="A Look At Crimes in Chicago and Hyde Park From 2015 to 2020",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Chicago', x=0.16, y=1, font_size=20, showarrow=False),
                 dict(text='Hyde Park', x=0.85, y=1, font_size=20, showarrow=False)])
st.plotly_chart(fig, use_container_width=True)
