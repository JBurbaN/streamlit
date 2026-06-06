import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

@st.cache_resource
def get_engine():

    user = st.secrets["DB_USER"]
    password = st.secrets["DB_PASSWORD"]
    host = st.secrets["DB_HOST"]
    port = st.secrets["DB_PORT"]
    database = st.secrets["DB_NAME"]

    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )

@st.cache_data(ttl=300)
def query(sql):
    return pd.read_sql(
        sql,
        get_engine()
    )