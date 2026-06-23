import os
import geopandas as gpd

kml_path = r"C:\Users\mgvin\Desktop\wb-analysis\data\raw\tn_constituencies.kml"
output_path = r"C:\Users\mgvin\Desktop\wb-analysis\data\spatial\tn_constituencies.geojson"

print("File Exists?", os.path.exists(kml_path))

gdf = gpd.read_file(kml_path)

print(f"Features Found: {len(gdf)}")
print("Columns:", gdf.columns.tolist())
print(gdf.head())

gdf.to_file(output_path, driver="GeoJSON")
print(f"\nSaved: {output_path}")