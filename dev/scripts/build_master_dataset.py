import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_2021 = BASE_DIR / "data" / "cleaned" / "wb_2021_raw.csv"
FILE_2026 = BASE_DIR / "data" / "cleaned" / "wb_2026_raw.csv"

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "wb_master_election.csv"

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df21 = pd.read_csv(FILE_2021)
df26 = pd.read_csv(FILE_2026)

# --------------------------------------------------
# Validation
# --------------------------------------------------

assert len(df21) == 294, f"2021 rows = {len(df21)}"
assert len(df26) == 294, f"2026 rows = {len(df26)}"

assert df21["Constituency_No"].nunique() == 294
assert df26["Constituency_No"].nunique() == 294

# --------------------------------------------------
# Select Required Columns
# --------------------------------------------------

df21 = df21[
    [
        "Constituency_No",
        "Constituency_Name",
        "District",
        "Winner_Candidate",
        "Winner_Party",
        "Winner_Votes",
        "Winner_Pct",
        "Margin",
    ]
].rename(
    columns={
        "Winner_Candidate": "Winner_Candidate_2021",
        "Winner_Party": "Winner_Party_2021",
        "Winner_Votes": "Winner_Votes_2021",
        "Winner_Pct": "Winner_Pct_2021",
        "Margin": "Margin_2021",
    }
)

df26 = df26[
    [
        "Constituency_No",
        "Winner_Candidate",
        "Winner_Party",
        "Winner_Votes",
        "Winner_Pct",
        "Margin",
    ]
].rename(
    columns={
        "Winner_Candidate": "Winner_Candidate_2026",
        "Winner_Party": "Winner_Party_2026",
        "Winner_Votes": "Winner_Votes_2026",
        "Winner_Pct": "Winner_Pct_2026",
        "Margin": "Margin_2026",
    }
)

# --------------------------------------------------
# Merge
# --------------------------------------------------

master = df21.merge(
    df26,
    on="Constituency_No",
    how="inner",
    validate="one_to_one"
)

# --------------------------------------------------
# Column Order
# --------------------------------------------------

master = master[
    [
        "Constituency_No",
        "Constituency_Name",
        "District",
        "Winner_Candidate_2021",
        "Winner_Party_2021",
        "Winner_Votes_2021",
        "Winner_Pct_2021",
        "Margin_2021",
        "Winner_Candidate_2026",
        "Winner_Party_2026",
        "Winner_Votes_2026",
        "Winner_Pct_2026",
        "Margin_2026",
    ]
]

# --------------------------------------------------
# Save
# --------------------------------------------------

master.to_csv(OUTPUT_FILE, index=False)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("=" * 60)
print("MASTER DATASET CREATED")
print("=" * 60)

print(f"Rows    : {len(master)}")
print(f"Columns : {len(master.columns)}")

print("\nFirst 5 Rows:")
print(master.head())

print(f"\nSaved to:\n{OUTPUT_FILE}")