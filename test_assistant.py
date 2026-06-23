from engine.data_loader import load_geojson
from engine.assistant_engine import answer_query

gdf = load_geojson()

response = answer_query("Explain Kalimpong", gdf)

print(response)