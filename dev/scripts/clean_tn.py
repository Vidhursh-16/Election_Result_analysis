import pandas as pd

# ── LOAD RAW FILES ────────────────────────────────
df_2026 = pd.read_csv(r"C:\Users\mgvin\Desktop\wb-analysis\data\raw\tn_2026_raw.csv")
df_2021 = pd.read_csv(r"C:\Users\mgvin\Desktop\wb-analysis\data\raw\tn_2021_raw.csv")

# ── PROCESS 2021 — Extract Winner + Runner ────────
# Winner rows
winners_2021 = df_2021[df_2021['Win_Lost_Flag'] == True].copy()
winners_2021 = winners_2021[['Constituency', 'Candidate', 'Party', 'Total_Votes', '%_of_Votes', 'Winning_votes']].copy()
winners_2021.columns = ['Constituency_Name', 'Winner_Candidate_2021', 'Winner_Party_2021', 'Winner_Votes_2021', 'Winner_Pct_2021', 'Margin_2021']

# Runner up — second highest votes per constituency
df_2021_sorted = df_2021.sort_values(['Constituency', 'Total_Votes'], ascending=[True, False])
runners_2021 = df_2021_sorted.groupby('Constituency').nth(1).reset_index()
runners_2021 = runners_2021[['Constituency', 'Candidate', 'Party', 'Total_Votes']].copy()
runners_2021.columns = ['Constituency_Name', 'Runner_Candidate_2021', 'Runner_Party_2021', 'Runner_Votes_2021']

# Merge winner + runner
df_2021_clean = pd.merge(winners_2021, runners_2021, on='Constituency_Name', how='left')
print(f"2021 clean — {len(df_2021_clean)} rows")
print(df_2021_clean.head(3))

# ── PROCESS 2026 ──────────────────────────────────
df_2026_clean = df_2026[[
    'District', 'Constituency_No', 'Constituency_Name',
    'Winner_Candidate', 'Winner_Party_Full', 'Winner_Votes',
    'Winner_Pct', 'Runner_Candidate', 'Runner_Party_Full',
    'Runner_Votes', 'Margin'
]].copy()

df_2026_clean.columns = [
    'District', 'Constituency_No', 'Constituency_Name',
    'Winner_Candidate_2026', 'Winner_Party_2026', 'Winner_Votes_2026',
    'Winner_Pct_2026', 'Runner_Candidate_2026', 'Runner_Party_2026',
    'Runner_Votes_2026', 'Margin_2026'
]

# Strip SC/ST tags from constituency name for merging
df_2026_clean['Constituency_Name_Clean'] = df_2026_clean['Constituency_Name'].str.replace(r'\s*\(SC\)|\s*\(ST\)', '', regex=True).str.strip()
df_2021_clean['Constituency_Name_Clean'] = df_2021_clean['Constituency_Name'].str.strip()

print(f"\n2026 clean — {len(df_2026_clean)} rows")
print(df_2026_clean.head(3))

# ── MERGE 2021 + 2026 ─────────────────────────────
df_merged = pd.merge(
    df_2026_clean,
    df_2021_clean,
    on='Constituency_Name_Clean',
    how='left'
)

# ── DERIVED COLUMNS ───────────────────────────────
df_merged['Margin_2026'] = pd.to_numeric(df_merged['Margin_2026'], errors='coerce')
df_merged['Margin_2021'] = pd.to_numeric(df_merged['Margin_2021'], errors='coerce')
df_merged['Winner_Pct_2026'] = pd.to_numeric(df_merged['Winner_Pct_2026'], errors='coerce')
df_merged['Winner_Pct_2021'] = pd.to_numeric(df_merged['Winner_Pct_2021'], errors='coerce')

df_merged['Margin_Change'] = df_merged['Margin_2026'] - df_merged['Margin_2021']
df_merged['Vote_Swing'] = df_merged['Winner_Pct_2026'] - df_merged['Winner_Pct_2021']

df_merged['Seat_Status'] = df_merged.apply(
    lambda r: 'Retained' if r['Winner_Party_2026'] == r['Winner_Party_2021'] else 'Flipped', axis=1
)
df_merged['Party_Change'] = df_merged['Winner_Party_2021'].fillna('Unknown') + ' → ' + df_merged['Winner_Party_2026'].fillna('Unknown')
# ── SAVE ──────────────────────────────────────────
df_merged.to_csv(r"C:\Users\mgvin\Desktop\wb-analysis\data\cleaned\tn_merged.csv", index=False)
print(f"\nMerged — {len(df_merged)} rows saved to data/cleaned/tn_merged.csv")
print(df_merged[['Constituency_Name_Clean', 'Winner_Party_2021', 'Winner_Party_2026', 'Seat_Status']].head(10))