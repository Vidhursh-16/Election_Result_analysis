import geopandas as gpd

# --------------------------------------------------
# LOAD GEOJSON
# --------------------------------------------------

gdf = gpd.read_file("../../data/spatial/tn_master.geojson")
# --------------------------------------------------
# DISTRICT -> REGION
# --------------------------------------------------

region_map = {

    # Chennai Region
    "CHENNAI": "Chennai",
    "THIRUVALLUR": "Chennai",
    "KANCHEEPURAM": "Chennai",

    # North Region
    "VELLORE": "North",
    "TIRUVANNAMALAI": "North",
    "VILUPPURAM": "North",
    "CUDDALORE": "North",
    "DHARMAPURI": "North",
    "KRISHNAGIRI": "North",

    # Western Region
    "COIMBATORE": "West",
    "ERODE": "West",
    "SALEM": "West",
    "NAMAKKAL   *": "West",
    "THE NILGIRIS": "West",

    # Central Region
    "TIRUCHIRAPPALLI": "Central",
    "KARUR  *": "Central",
    "PERAMBALUR": "Central",

    # Delta Region
    "THANJAVUR": "Delta",
    "THIRUVARUR": "Delta",
    "NAGAPATTINAM  *": "Delta",

    # South Region
    "MADURAI": "South",
    "DINDIGUL": "South",
    "THENI  *": "South",
    "SIVAGANGA": "South",
    "RAMANATHAPURAM": "South",
    "VIRUDHUNAGAR": "South",
    "THOOTHUKKUDI": "South",
    "TIRUNELVELI": "South",
    "KANNIYAKUMARI": "South",

    # South-Central
    "PUDUKKOTTAI": "South-Central",

}

# --------------------------------------------------
# ADD REGION COLUMN
# --------------------------------------------------

gdf["Region"] = gdf["dist_name"].map(region_map)

# Fill unknown districts

gdf["Region"] = gdf["Region"].fillna("Unknown")

# --------------------------------------------------
# SAVE
# --------------------------------------------------

gdf.to_file(
    "../../data/spatial/tn_master.geojson",
    driver="GeoJSON"
)

print("✅ Region column added successfully.")
print(gdf[["dist_name", "Region"]].drop_duplicates().sort_values("dist_name"))
print(gdf[gdf["Region"] == "Unknown"]["dist_name"].unique())
print(gdf[["ac_name", "dist_name", "Region"]].head(20))