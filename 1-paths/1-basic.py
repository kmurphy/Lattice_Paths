import streamlit as st

from common import * 

st.title(f"Count Paths")

import paths.dyck as dyck
import paths.motzkin as motzkin 
import paths.schroder as schroder 
import paths.motzkin_schroder as motzkin_schroder 

path_types = {
    'Dyck': dyck,
    'Motzkin': motzkin,
    'Schröder': schroder,
    'Motzkin-Schröder': motzkin_schroder,
}

df_tmp = pd.read_feather(f'data/motzkin_schroder.feather')
properties = df_tmp.columns[2:].tolist()

path_type = st.selectbox('Select Path:', path_types.keys())

ph = path_types[path_type]


df_all = pd.read_feather(f'data/{ph.SAFE_NAME}.feather')

st.write("## Count/Draw Paths")

# properties = df_all.columns[2:].tolist()

# help = ("Write any valid pandas query using columns: " 
#     + ','.join([f"`{c}`" for c in properties]) 
#     )
# criteria = st.text_input('Filter:', value='n==3', help=help)
# try:
#     df = df_all.query(criteria)
# except ValueError:
#     st.error("Not a valid query criteria, Look like you have used = in place of ==")    
#     criteria = 'n==4'
# st.write(f'Using query criteria: {criteria}')
n = st.slider("Length:", min_value=0, max_value=df_all.n.max())
df = df_all.query('n==@n')

st.write(f'Number of paths: {df.shape[0]}')

properties_selected = st.multiselect("Group by (order selected is important):", options=properties)


if properties_selected:
    df_layout = layout_by_feature(df, properties_selected)

    # st.dataframe(df_layout)

    title = "by " + ", ".join(properties_selected)
    if df_layout.shape[0]:
        fig = layout_paths(ph, df_layout, title_postfix=title)
        st.pyplot(fig)