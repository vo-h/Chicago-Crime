# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 01:24:01 2021

@author: hienv
"""

import os
import streamlit as st
from google.cloud import bigquery
from prevalent_crime import prevalent_crime
from crime_over_time import crime_over_time
from crime_by_week import crime_by_week
from crime_by_hour import crime_by_hour

st.title("Chicago Crime")

if os.path.isfile("google-credentials.json"):

    # Set up Google Cloud
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"
    client = bigquery.Client()

    # Get some relevant variables
    max_year = int(
        client.query(
            """SELECT max(year) FROM `bigquery-public-data.chicago_crime.crime`"""
        )
        .to_dataframe()
        .loc[0, "f0_"]
    )
    min_year = int(
        client.query(
            """SELECT min(year) FROM `bigquery-public-data.chicago_crime.crime`"""
        )
        .to_dataframe()
        .loc[0, "f0_"]
    )
    
    # Add image
    st.sidebar.image("image.jpg")

    # Set up side bar
    question = st.sidebar.selectbox(
        "Choose Categories You Want To Explore",
        ("Prevalent Crime", "Crime Over Time", "Crime by Weekday", "Crime by Time of Day"),
    )

    # Initiate a slidebar to get year range
    year_range = st.sidebar.slider(
        "Select range of year", min_year, max_year, (2015, max_year)
    )

    # Allow user to include domestic
    exclude_domestic = st.sidebar.checkbox("Exclude Domestic Crimes", value=True)

    if question == "Prevalent Crime":

        # Produce plotly plots from options
        prevalent_crime(
            client=client, year_range=year_range, exclude_domestic=exclude_domestic
        )

    if question in ["Crime Over Time", "Crime by Weekday", "Crime by Time of Day"]:

        # Provide choices
        st.sidebar.write(" ")

        crimes_dict = {
            "THEFT": st.sidebar.checkbox("Theft", value=True),
            "BATTERY": st.sidebar.checkbox("Battery"),
            "CRIMINAL DAMAGE": st.sidebar.checkbox("Criminal Damage"),
            "NARCOTICS": st.sidebar.checkbox("Narcotics"),
            "BURGLARY": st.sidebar.checkbox("Burglary"),
            "ASSAULT": st.sidebar.checkbox("Assault"),
            "ROBBERY": st.sidebar.checkbox("Robbery"),
        }

        if question == "Crime Over Time":

            crime_over_time(client, year_range, exclude_domestic, crimes_dict)

        if question == "Crime by Weekday":

            crime_by_week(client, year_range, exclude_domestic, crimes_dict)

        if question == "Crime by Time of Day":

            crime_by_hour(client, year_range, exclude_domestic, crimes_dict)
