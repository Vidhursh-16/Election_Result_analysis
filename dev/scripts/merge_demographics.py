import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Files
master_file = (
    BASE_DIR /
    "data" /
    "processed" /
    "wb_master_analysis.csv"
)

demographics_file = (
    BASE_DIR /
    "data" /
    "WB_District_Analysis.xlsx"
)

output_file = (
    BASE_DIR /
    "data" /
    "processed" /
    "wb_demographic_master.csv"
)

# Load
master = pd.read_csv(master_file)

demographics = pd.read_excel(
    demographics_file,
    sheet_name="WB_District_Data"
)

# Merge
merged = master.merge(
    demographics,
    on="District",
    how="left",
    validate="many_to_one"
)

# Validation
print("=" * 60)
print("MERGE VALIDATION")
print("=" * 60)

print("Rows:", len(merged))
print("Columns:", len(merged.columns))

print("\nMissing Demographics:")
print(
    merged[
        [
            "Minority_Pct",
            "Women_Voter_Pct",
            "Unemployment_Pct",
            "SIR_Risk"
        ]
    ].isna().sum()
)

# Save
merged.to_csv(output_file, index=False)

print(f"\nSaved:\n{output_file}")