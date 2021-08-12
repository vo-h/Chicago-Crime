# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 01:24:01 2021

@author: hienv
"""

import streamlit as st
import os

st.title("Chicago Crime")


if os.path.isfile('google-credentials.json'):
    st.write('here')