import streamlit as st
import geopandas as gpd


@st.cache_data
@st.cache_data
@st.cache_data
def load_geojson(state="wb"):
    path = "data/spatial/wb_master_geojson.geojson" if state == "wb" else "data/spatial/tn_master.geojson"
    return gpd.read_file(path)

print("loaded sucessfully")