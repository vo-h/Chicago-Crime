# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 15:59:15 2021

@author: hienv
"""

import streamlit as st
import plotly.express as px


def crime_over_time(client, year_range, exclude_domestic, crimes_dict):
    """
    Produce line charts of crime in chicago & hyde park in year_range
    """

    # Assemble SQL queries
    sql_chicago = "select format_date('%Y-%m', datetime(date, 'US/Central')) as date"
    sql_hp = "select format_date('%Y-%m', datetime(date, 'US/Central')) as date"
    for crime in crimes_dict:
        if crimes_dict[crime]:
            sql_chicago += f""", count(case when primary_type = '{crime}'
            {'and domestic = False' if exclude_domestic else ''} 
            then 1 end) as {crime.replace(' ', '_').lower()}"""
            sql_hp += f""", count(case when primary_type = '{crime}'
            {'and domestic = False' if exclude_domestic else ''} then 1 end)
            as {crime.replace(' ', '_').lower()}"""

    sql_chicago += f""" from `bigquery-public-data.chicago_crime.crime`
    where year between {year_range[0]} and {year_range[1]} group by 1;"""
    sql_hp += f""" from `bigquery-public-data.chicago_crime.crime`
    where year between {year_range[0]} and {year_range[1]} and community_area=41 
    group by 1;"""

    # Get data
    chicago = (
        client.query(sql_chicago).to_dataframe().sort_values("date", ignore_index=True)
    )
    hyde_park = (
        client.query(sql_hp).to_dataframe().sort_values("date", ignore_index=True)
    )

    # Visualize with plotly
    fig1 = px.line(
        chicago,
        x="date",
        y=chicago.columns,
        title=f"A Look of Select Crimes in Chicago from {year_range[0]} to {year_range[1]}",
        labels={"value": "monthly count"},
    )

    fig2 = px.line(
        hyde_park,
        x="date",
        y=hyde_park.columns,
        title=f"A Look of Select Crimes in Hyde Park from {year_range[0]} to {year_range[1]}",
        labels={"value": "monthly count"},
    )

    # Fix fig size
    fig1.update_layout(
        autosize=False,
        width=800,
        height=800,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        paper_bgcolor="LightSteelBlue",
    )
    fig2.update_layout(
        autosize=False,
        width=800,
        height=800,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        paper_bgcolor="LightSteelBlue",
    )

    # Plot data
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
