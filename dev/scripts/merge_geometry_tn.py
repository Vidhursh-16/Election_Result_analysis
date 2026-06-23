import pandas as pd
import geopandas as gpd
import re

# ── LOAD ──────────────────────────────────────────
gdf = gpd.read_file(r"C:\Users\mgvin\Desktop\wb-analysis\data\spatial\tn_constituencies.geojson")
df = pd.read_csv(r"C:\Users\mgvin\Desktop\wb-analysis\data\cleaned\tn_merged.csv")

# ── CLEAN MERGE KEYS ──────────────────────────────
gdf['ac_name_clean'] = gdf['ac_name'].str.strip().str.upper()
gdf['ac_name_clean'] = gdf['ac_name_clean'].str.replace(r'\s*\(SC\)|\s*\(ST\)', '', regex=True).str.strip()

# Manual name corrections — GDF → CSV
name_map = {
    'GUMMIDIPOONDI': 'GUMMIDIPUNDI',
    'TIRUVOTTIYUR': 'THIRUVOTTIYUR',
    'SHOLINGUR': 'SHOLINGHUR',
    'DR.RADHAKRISHNAN NAGA': 'DR RADHAKRISHNAN NAGAR',
    'KILVAITHINANKUPPAM(SC': 'KILVAITHINANKUPPAM',
    'VIRUGAMPAKKAM': 'VIRUGAMBAKKAM',
    'CHEPAUK-THIRUVALLIKEN': 'CHEPAUK THIRUVALLIKENI',
    'VILUPPURAM': 'VILLUPURAM',
    'PALACODU': 'PALAKODU',
    'VRIDDHACHALAM': 'VRIDHACHALAM',
    'COIMBATORE(NORTH)': 'COIMBATORE NORTH',
    'METTUPPALAYAM': 'METTUPALAYAM',
    'TIRUCHIRAPPALLI': 'TIRUCHIRAPPALI',
    'COIMBATORE(SOUTH)': 'COIMBATORE SOUTH',
    'MANAPPARAI': 'MANAPPARAI',
    'GANDHARVAKOTTAI': 'GANDARVAKOTTAI',
    'NILAKKOTTAI': 'NILAKOTTAI',
    'COLACHEL': 'KULACHAL',
}

gdf['ac_name_clean'] = gdf['ac_name_clean'].replace(name_map)
df['Constituency_Name_Clean'] = df['Constituency_Name_Clean'].str.strip().str.upper()

# ── CHECK BEFORE MERGE ────────────────────────────
print(f"GDF rows: {len(gdf)}")
print(f"CSV rows: {len(df)}")
print(f"\nSample GDF names: {gdf['ac_name_clean'].head(5).tolist()}")
print(f"Sample CSV names: {df['Constituency_Name_Clean'].head(5).tolist()}")

# ── MERGE ─────────────────────────────────────────
merged_gdf = gdf.merge(df, left_on='ac_name_clean', right_on='Constituency_Name_Clean', how='left')

print(f"\nMerged rows: {len(merged_gdf)}")
print(f"Null Winner_Party_2026: {merged_gdf['Winner_Party_2026'].isna().sum()}")

# Find unmatched
unmatched = merged_gdf[merged_gdf['Winner_Party_2026'].isna()][['ac_name_clean']].drop_duplicates()
print("\nUnmatched constituencies:")
print(unmatched.to_string())

# Find duplicates
dupes = merged_gdf[merged_gdf.duplicated('ac_name_clean', keep=False)][['ac_name_clean']].drop_duplicates()
print("\nDuplicate matches:")
print(dupes.to_string())

# ── SAVE ──────────────────────────────────────────
merged_gdf.to_file(
    r"C:\Users\mgvin\Desktop\wb-analysis\data\spatial\tn_master.geojson",
    driver="GeoJSON"
)
print("\nSaved: data/spatial/tn_master.geojson")