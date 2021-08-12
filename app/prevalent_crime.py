# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 14:37:55 2021

@author: hienv
"""

import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def prevalent_crime(client, year_range, exclude_domestic):
    """
    Produce pie charts of crime in chicago and hyde park with a year_range
    """

    # Assemble sql queries
    sql_chicago = f"""select primary_type, count(primary_type) as count
            from `bigquery-public-data.chicago_crime.crime` 
            where year between {year_range[0]} and {year_range[1]}
            {'and domestic = False' if exclude_domestic else ''}
            group by 1;"""
    sql_hp = f"""select primary_type, count(primary_type) as count
            from `bigquery-public-data.chicago_crime.crime` 
            where year between {year_range[0]} and {year_range[1]}
            and community_area = 41
            {'and domestic = False' if exclude_domestic else ''}
            group by 1;"""

    # Get data
    chicago = client.query(sql_chicago).to_dataframe()
    hyde_park = client.query(sql_hp).to_dataframe()

    # Group crimes that are rare
    chicago.loc[
        chicago["count"] < float(chicago.quantile(0.6)), "primary_type"
    ] = "OTHER OFFENSE"
    hyde_park.loc[
        hyde_park["count"] < float(hyde_park.quantile(0.6)), "primary_type"
    ] = "OTHER OFFENSE"

    # Create subplots: use 'domain' type for pie subplot
    fig = make_subplots(
        rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
    )
    fig.add_trace(
        go.Pie(labels=chicago["primary_type"], values=chicago["count"], name=""), 1, 1
    )
    fig.add_trace(
        go.Pie(labels=hyde_park["primary_type"], values=hyde_park["count"], name=""),
        1,
        2,
    )

    # Add some frills
    fig.update_layout(
        title_text=f"Prevalent Crime in Chicago and Hyde Park Between {year_range[0]} and {year_range[1]}",
        width=800,
        height=500,
        annotations=[
            dict(text="Chicago", x=0.12, y=1, font_size=20, showarrow=False),
            dict(text="Hyde Park", x=0.89, y=1, font_size=20, showarrow=False),
        ],
    )

    # Display plot
    st.plotly_chart(fig)
