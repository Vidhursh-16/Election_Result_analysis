import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "wb_master_analysis.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "districts.csv"
)

df = pd.read_csv(INPUT_FILE)

districts = sorted(df["District"].unique())

district_df = pd.DataFrame({
    "District": districts
})

district_df.to_csv(OUTPUT_FILE, index=False)

print(f"District Count: {len(districts)}")
print("\nDistricts:")
print(district_df)

print(f"\nSaved to: {OUTPUT_FILE}")