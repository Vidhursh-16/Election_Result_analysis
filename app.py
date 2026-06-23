import streamlit as st
from engine.data_loader import load_geojson
from ui.home import render_home
from ui.home_tn import render_home_tn

st.set_page_config(page_title="Election Intelligence Platform", layout="wide")

state = st.sidebar.radio("Select State", ["West Bengal", "Tamil Nadu"])

if state == "West Bengal":
    gdf = load_geojson()
    render_home(gdf)
else:
    gdf = st.cache_data(lambda: __import__('geopandas').read_file(
        r"C:\Users\mgvin\Desktop\wb-analysis\data\spatial\tn_master.geojson"
    ))()
    render_home_tn(gdf)