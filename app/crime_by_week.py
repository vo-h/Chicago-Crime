# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 16:30:10 2021

@author: hienv
"""

import streamlit as st
import plotly.express as px


def crime_by_week(client, year_range, exclude_domestic, crimes_dict):
    """
    Produce bar charts by weekday in chicago & hyde park in year_range
    """

    # Assemble SQL queries
    sql_chicago = (
        "select format_date('%a', datetime(date, 'US/Central')) as day_of_week"
    )
    sql_hp = "select format_date('%a', datetime(date, 'US/Central')) as day_of_week"
    for crime in crimes_dict:
        if crimes_dict[crime]:
            sql_chicago += f""", count(case when primary_type = '{crime}'
            {'and domestic = False' if exclude_domestic else ''} then 1 end)
            as {crime.replace(' ', '_').lower()}"""
            sql_hp += f""", count(case when primary_type = '{crime}'
            {'and domestic = False' if exclude_domestic else ''} then 1 end)
            as {crime.replace(' ', '_').lower()}"""

    sql_chicago += f""" from `bigquery-public-data.chicago_crime.crime`
    where year between {year_range[0]} and {year_range[1]} group by 1;"""
    sql_hp += f""" from `bigquery-public-data.chicago_crime.crime`
    where year between {year_range[0]} and {year_range[1]} and community_area=41 group by 1;"""

    # Get data
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hyde_park = (
        client.query(sql_hp).to_dataframe().set_index("day_of_week").reindex(days)
    )
    chicago = (
        client.query(sql_chicago).to_dataframe().set_index("day_of_week").reindex(days)
    )

    # Create plots
    fig1 = px.bar(
        chicago,
        x=chicago.index,
        y=chicago.columns,
        title=f"Crimes in Chicago by Day from {year_range[0]} to {year_range[1]}",
        labels={"value": "count"},
    )
    fig2 = px.bar(
        hyde_park,
        x=hyde_park.index,
        y=hyde_park.columns,
        title=f"Crimes in Hyde Park by Day from {year_range[0]} to {year_range[1]}",
        labels={"value": "count"},
    )

    # Fix fig size
    fig1.update_layout(
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )
    fig2.update_layout(
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )

    # Plot
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
