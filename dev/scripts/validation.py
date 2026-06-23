import geopandas as gpd
gdf = gpd.read_file(r"C:\Users\mgvin\Desktop\wb-analysis\data\spatial\tn_master.geojson")
print([c for c in gdf.columns if 'Region' in c or 'region' in c])