import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "wb_master_election.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "wb_master_analysis.csv"
)

# --------------------------------------------------
# Load
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# Features
# --------------------------------------------------

df["Seat_Status"] = (
    df["Winner_Party_2021"]
    == df["Winner_Party_2026"]
).map({
    True: "Retained",
    False: "Flipped"
})

df["Party_Change"] = (
    df["Winner_Party_2021"]
    + " → "
    + df["Winner_Party_2026"]
)

df["Vote_Swing"] = (
    df["Winner_Pct_2026"]
    - df["Winner_Pct_2021"]
)

df["Margin_Change"] = (
    df["Margin_2026"]
    - df["Margin_2021"]
)

# Round swing for readability
df["Vote_Swing"] = df["Vote_Swing"].round(2)

# --------------------------------------------------
# Save
# --------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("=" * 60)
print("MASTER ANALYSIS DATASET CREATED")
print("=" * 60)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print("\nSeat Status:")
print(df["Seat_Status"].value_counts())

print(f"\nSaved:\n{OUTPUT_FILE}")