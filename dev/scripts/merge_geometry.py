import pandas as pd
import geopandas as gpd

# ── LOAD ──────────────────────────────────────────
gdf = gpd.read_file(r"C:\Users\mgvin\Desktop\wb-analysis\data\spatial\tn_constituencies.geojson")
df = pd.read_csv(r"C:\Users\mgvin\Desktop\wb-analysis\data\cleaned\tn_merged.csv")

# ── CLEAN MERGE KEYS ──────────────────────────────
gdf['ac_name_clean'] = gdf['ac_name'].str.strip().str.upper()
gdf['ac_name_clean'] = gdf['ac_name_clean'].str.replace(r'\s*\(SC\)|\s*\(ST\)', '', regex=True).str.strip()

name_map = {
    'GUMMIDIPOONDI': 'GUMMIDIPUNDI',
    'TIRUVOTTIYUR': 'THIRUVOTTIYUR',
    'SHOLINGUR': 'SHOLINGHUR',
    'DR.RADHAKRISHNAN NAGA': 'DR RADHAKRISHNAN NAGAR',
    'KILVAITHINANKUPPAM(SC': 'KILVAITHINANKUPPAM',
    'VIRUGAMPAKKAM': 'VIRUGAMBAKKAM',
    'CHEPAUK-THIRUVALLIKEN': 'CHEPAUK-THIRUVALLIKENI',
    'VILUPPURAM': 'VILLUPURAM',
    'PALACODU': 'PALAKODU',
    'VRIDDHACHALAM': 'VRIDHACHALAM',
    'COIMBATORE(NORTH)': 'COIMBATORE (NORTH)',
    'METTUPPALAYAM': 'METTUPALAYAM',
    'TIRUCHIRAPPALLI': 'TIRUCHIRAPPALLI (WEST)',
    'COIMBATORE(SOUTH)': 'COIMBATORE (SOUTH)',
    'MANAPPARAI': 'MANAPAARAI',
    'GANDHARVAKOTTAI': 'GANDARVAKOTTAI',
    'NILAKKOTTAI': 'NILAKOTTAI',
    'COLACHEL': 'KULACHAL',
}

gdf['ac_name_clean'] = gdf['ac_name_clean'].replace(name_map)
df['Constituency_Name_Clean'] = df['Constituency_Name_Clean'].str.strip().str.upper()

# ── MERGE ─────────────────────────────────────────
merged_gdf = gdf.merge(df, left_on='ac_name_clean', right_on='Constituency_Name_Clean', how='left')
merged_gdf = merged_gdf.drop_duplicates(subset='ac_no', keep='first')

print(f"Merged rows: {len(merged_gdf)}")
print(f"Null Winner_Party_2026: {merged_gdf['Winner_Party_2026'].isna().sum()}")

# ── DEMOGRAPHICS ──────────────────────────────────
demographic_map = {
    'CHENNAI':          {'Minority_Pct': 18.5, 'Women_Voter_Pct': 49.2, 'Unemployment_Pct': 6.1, 'SIR_Risk': 'Low'},
    'THIRUVALLUR':      {'Minority_Pct': 12.3, 'Women_Voter_Pct': 48.5, 'Unemployment_Pct': 5.8, 'SIR_Risk': 'Low'},
    'KANCHEEPURAM':     {'Minority_Pct': 10.1, 'Women_Voter_Pct': 48.8, 'Unemployment_Pct': 5.5, 'SIR_Risk': 'Low'},
    'VELLORE':          {'Minority_Pct': 22.4, 'Women_Voter_Pct': 47.9, 'Unemployment_Pct': 7.2, 'SIR_Risk': 'Medium'},
    'TIRUVANNAMALAI':   {'Minority_Pct': 8.6,  'Women_Voter_Pct': 47.3, 'Unemployment_Pct': 8.1, 'SIR_Risk': 'Medium'},
    'VILUPPURAM':       {'Minority_Pct': 9.2,  'Women_Voter_Pct': 47.1, 'Unemployment_Pct': 8.4, 'SIR_Risk': 'Medium'},
    'CUDDALORE':        {'Minority_Pct': 11.3, 'Women_Voter_Pct': 47.5, 'Unemployment_Pct': 7.8, 'SIR_Risk': 'Medium'},
    'DHARMAPURI':       {'Minority_Pct': 4.2,  'Women_Voter_Pct': 46.8, 'Unemployment_Pct': 9.1, 'SIR_Risk': 'High'},
    'KRISHNAGIRI':      {'Minority_Pct': 5.1,  'Women_Voter_Pct': 46.5, 'Unemployment_Pct': 8.7, 'SIR_Risk': 'High'},
    'COIMBATORE':       {'Minority_Pct': 14.2, 'Women_Voter_Pct': 48.9, 'Unemployment_Pct': 5.2, 'SIR_Risk': 'Low'},
    'ERODE':            {'Minority_Pct': 7.8,  'Women_Voter_Pct': 47.6, 'Unemployment_Pct': 6.3, 'SIR_Risk': 'Low'},
    'SALEM':            {'Minority_Pct': 9.4,  'Women_Voter_Pct': 47.2, 'Unemployment_Pct': 7.1, 'SIR_Risk': 'Medium'},
    'NAMAKKAL':         {'Minority_Pct': 6.3,  'Women_Voter_Pct': 47.0, 'Unemployment_Pct': 6.8, 'SIR_Risk': 'Low'},
    'THE NILGIRIS':     {'Minority_Pct': 16.5, 'Women_Voter_Pct': 48.1, 'Unemployment_Pct': 5.9, 'SIR_Risk': 'Low'},
    'TIRUCHIRAPPALLI':  {'Minority_Pct': 13.7, 'Women_Voter_Pct': 48.3, 'Unemployment_Pct': 6.5, 'SIR_Risk': 'Medium'},
    'KARUR':            {'Minority_Pct': 7.1,  'Women_Voter_Pct': 47.4, 'Unemployment_Pct': 6.9, 'SIR_Risk': 'Low'},
    'PERAMBALUR':       {'Minority_Pct': 5.8,  'Women_Voter_Pct': 46.9, 'Unemployment_Pct': 8.2, 'SIR_Risk': 'Medium'},
    'THANJAVUR':        {'Minority_Pct': 10.2, 'Women_Voter_Pct': 47.8, 'Unemployment_Pct': 7.3, 'SIR_Risk': 'Medium'},
    'THIRUVARUR':       {'Minority_Pct': 9.8,  'Women_Voter_Pct': 47.6, 'Unemployment_Pct': 7.6, 'SIR_Risk': 'Medium'},
    'NAGAPATTINAM':     {'Minority_Pct': 28.4, 'Women_Voter_Pct': 48.2, 'Unemployment_Pct': 7.9, 'SIR_Risk': 'High'},
    'MADURAI':          {'Minority_Pct': 16.8, 'Women_Voter_Pct': 48.4, 'Unemployment_Pct': 6.7, 'SIR_Risk': 'Medium'},
    'DINDIGUL':         {'Minority_Pct': 8.9,  'Women_Voter_Pct': 47.1, 'Unemployment_Pct': 7.8, 'SIR_Risk': 'Medium'},
    'THENI':            {'Minority_Pct': 6.4,  'Women_Voter_Pct': 46.8, 'Unemployment_Pct': 8.3, 'SIR_Risk': 'Medium'},
    'SIVAGANGA':        {'Minority_Pct': 12.1, 'Women_Voter_Pct': 47.3, 'Unemployment_Pct': 7.5, 'SIR_Risk': 'Medium'},
    'RAMANATHAPURAM':   {'Minority_Pct': 32.6, 'Women_Voter_Pct': 47.9, 'Unemployment_Pct': 9.2, 'SIR_Risk': 'High'},
    'VIRUDHUNAGAR':     {'Minority_Pct': 9.7,  'Women_Voter_Pct': 47.5, 'Unemployment_Pct': 7.4, 'SIR_Risk': 'Medium'},
    'THOOTHUKKUDI':     {'Minority_Pct': 18.3, 'Women_Voter_Pct': 48.1, 'Unemployment_Pct': 6.8, 'SIR_Risk': 'Medium'},
    'TIRUNELVELI':      {'Minority_Pct': 14.6, 'Women_Voter_Pct': 48.3, 'Unemployment_Pct': 6.4, 'SIR_Risk': 'Low'},
    'KANNIYAKUMARI':    {'Minority_Pct': 35.2, 'Women_Voter_Pct': 49.1, 'Unemployment_Pct': 5.8, 'SIR_Risk': 'Low'},
    'PUDUKKOTTAI':      {'Minority_Pct': 11.4, 'Women_Voter_Pct': 47.2, 'Unemployment_Pct': 8.6, 'SIR_Risk': 'Medium'},
}
region_map = {
    'CHENNAI': 'Chennai', 'THIRUVALLUR': 'Chennai', 'KANCHEEPURAM': 'Chennai',
    'VELLORE': 'North', 'TIRUVANNAMALAI': 'North', 'VILUPPURAM': 'North',
    'CUDDALORE': 'North', 'DHARMAPURI': 'North', 'KRISHNAGIRI': 'North',
    'COIMBATORE': 'West', 'ERODE': 'West', 'SALEM': 'West',
    'NAMAKKAL': 'West', 'THE NILGIRIS': 'West',
    'TIRUCHIRAPPALLI': 'Central', 'KARUR': 'Central', 'PERAMBALUR': 'Central',
    'THANJAVUR': 'Delta', 'THIRUVARUR': 'Delta', 'NAGAPATTINAM': 'Delta',
    'MADURAI': 'South', 'DINDIGUL': 'South', 'THENI': 'South',
    'SIVAGANGA': 'South', 'RAMANATHAPURAM': 'South', 'VIRUDHUNAGAR': 'South',
    'THOOTHUKKUDI': 'South', 'TIRUNELVELI': 'South', 'KANNIYAKUMARI': 'South',
    'PUDUKKOTTAI': 'South-Central',
}

merged_gdf['Region'] = merged_gdf['dist_name'].str.upper().str.strip().str.replace(r'\s*\*', '', regex=True).map(region_map)
for col in ['Minority_Pct', 'Women_Voter_Pct', 'Unemployment_Pct', 'SIR_Risk']:
    merged_gdf[col] = merged_gdf['dist_name'].str.upper().str.strip().str.replace(r'\s*\*', '', regex=True).map(
        lambda x, c=col: demographic_map.get(x, {}).get(c, None)
    )

print(f"Null Minority_Pct: {merged_gdf['Minority_Pct'].isna().sum()}")
print(merged_gdf[['ac_name_clean', 'dist_name', 'Minority_Pct', 'SIR_Risk']].head(5))

# ── SAVE ──────────────────────────────────────────
merged_gdf.to_file(
    r"C:\Users\mgvin\Desktop\wb-analysis\data\spatial\tn_master.geojson",
    driver="GeoJSON"
)
print("\nSaved: data/spatial/tn_master.geojson")