import pandas as pd

def get_party_summary(gdf, party_name):
    party_df = gdf[gdf["Winner_Party_2026"] == party_name]

    seats = len(party_df)

    # Region
    if "Region" in party_df.columns and not party_df.empty:
        strongest_region = party_df["Region"].value_counts().idxmax()
    else:
        strongest_region = "N/A"

    # Margin — works for both WB and TN
    margin_col = "Margin_2026" if "Margin_2026" in party_df.columns else "Victory_Margin"
    if margin_col in party_df.columns and not party_df.empty:
        avg_margin = round(party_df[margin_col].mean(), 0)
    else:
        avg_margin = "N/A"

    # Top district
    if "District" in party_df.columns and not party_df.empty:
        top_district = party_df["District"].value_counts().idxmax()
    else:
        top_district = "N/A"

    # Vote share
    vote_col = "Winner_Votes_2026" if "Winner_Votes_2026" in gdf.columns else None
    if vote_col and not party_df.empty:
        total = gdf[vote_col].sum()
        party_total = party_df[vote_col].sum()
        vote_share = f"{round((party_total / total) * 100, 1)}%" if total > 0 else "N/A"
    else:
        vote_share = "N/A"

    return {
        "party": party_name,
        "seats": seats,
        "vote_share": vote_share,
        "strongest_region": strongest_region,
        "average_margin": avg_margin,
        "top_district": top_district,
    }


def get_constituency(gdf, constituency_name):
    col = "Constituency_Name_x" if "Constituency_Name_x" in gdf.columns else "Constituency_Name"
    constituency = gdf[gdf[col].str.lower() == constituency_name.lower()]
    if constituency.empty:
        return None
    return constituency.iloc[0].to_dict()