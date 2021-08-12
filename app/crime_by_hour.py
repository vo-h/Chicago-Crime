# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 16:50:41 2021

@author: hienv
"""

import streamlit as st
import plotly.express as px

def crime_by_hour(client, year_range, exclude_domestic, crimes_dict):
    # Assemble SQL queries
    sql_chicago = "select format_date('%H', datetime(date, 'US/Central')) as hour"
    sql_hp = "select format_date('%H', datetime(date, 'US/Central')) as hour"
    for crime in crimes_dict:
        if crimes_dict[crime]:
            sql_chicago += f", count(case when primary_type = '{crime}' {'and domestic = False' if exclude_domestic else ''} then 1 end) as {crime.replace(' ', '_').lower()}"
            sql_hp      += f", count(case when primary_type = '{crime}' {'and domestic = False' if exclude_domestic else ''} then 1 end) as {crime.replace(' ', '_').lower()}"
    
    sql_chicago += f" from `bigquery-public-data.chicago_crime.crime` where year between {year_range[0]} and {year_range[1]} group by 1;"
    sql_hp      += f" from `bigquery-public-data.chicago_crime.crime` where year between {year_range[0]} and {year_range[1]} and community_area=41 group by 1;"
    
    # Get data
    chicago = client.query(sql_chicago).to_dataframe().sort_values('hour', ignore_index=True).set_index('hour')
    hyde_park = client.query(sql_hp).to_dataframe().sort_values('hour', ignore_index=True).set_index('hour')
    
    # Create plots
    fig1 = px.bar(chicago, x=chicago.index, y=hyde_park.columns, title=f'Crime Count in Chicago by Hour from {year_range[0]} to {year_range[1]}')
    fig2 = px.bar(hyde_park, x=hyde_park.index, y=hyde_park.columns, title=f'Crime Count in Hyde Park by Hour from {year_range[0]} to {year_range[1]}')

    # Plot
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)