import streamlit as st

from common import *

page_dict = {}

page_dict['Paths'] = [
    st.Page('1-paths/1-basic.py', title='Counting Paths', icon=':material/help:'),
]

pg = st.navigation(page_dict)

pg.run()