import pandas as pd
import requests
from io import StringIO

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url_2026 = "https://en.wikipedia.org/wiki/2026_Tamil_Nadu_Legislative_Assembly_election#Results"

response_2026 = requests.get(url_2026, headers=headers)
tables_2026 = pd.read_html(StringIO(response_2026.text))

df_2026 = tables_2026[21]
df_2026 = df_2026.iloc[1:].reset_index(drop=True)

df_2026.columns = [
    'District', 'Constituency_No', 'Constituency_Name',
    'Winner_Candidate', 'Winner_Party', 'Winner_Party_Full',
    'Winner_Votes', 'Winner_Pct',
    'Runner_Candidate', 'Runner_Party', 'Runner_Party_Full',
    'Runner_Votes', 'Runner_Pct',
    'Margin'
]

df_2026['Year'] = 2026
df_2026.to_csv(r"C:\Users\mgvin\Desktop\wb-analysis\data\raw\tn_2026_raw.csv", index=False)
print(f"TN 2026 done — {len(df_2026)} rows saved")
print(df_2026.head(3))