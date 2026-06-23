import pandas as pd
import os

# Path to your CSV with the Region column
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
csv_path = os.path.join(project_root, 'data', 'processed', 'wb_demographic_master_with_region.csv')

# Load data
df = pd.read_csv(csv_path)

# 1. Show unique district-region mapping (one row per district)
district_region = df[['District', 'Region']].drop_duplicates().sort_values('District')
print("=== District to Region Mapping ===\n")
print(district_region.to_string(index=False))

# 2. Check for any district that appears with more than one region (inconsistency)
duplicate_check = district_region.groupby('District').filter(lambda x: len(x) > 1)
if not duplicate_check.empty:
    print("\n⚠️ WARNING: The following districts have inconsistent region assignments:\n")
    print(duplicate_check)
else:
    print("\n✅ All districts have a single, consistent region assignment.")

# 3. Check for any district not covered (Region = 'Other')
others = district_region[district_region['Region'] == 'Other']
if not others.empty:
    print("\n⚠️ WARNING: These districts were not matched to any region (labeled 'Other'):\n")
    print(others)
else:
    print("\n✅ All districts were matched to a specific region.")

# 4. Count of constituencies per region
print("\n=== Number of constituencies per region ===\n")
print(df['Region'].value_counts().to_string())

# 5. Optional: Show a sample of rows for each region
print("\n=== Sample rows from each region (first 2 per region) ===\n")
for region in df['Region'].unique():
    print(f"\n--- {region} ---")
    sample = df[df['Region'] == region][['Constituency_No', 'Constituency_Name', 'District', 'Region']].head(2)
    print(sample.to_string(index=False))