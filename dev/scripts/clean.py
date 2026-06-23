import pandas as pd

df = pd.read_csv(r"C:\Users\mgvin\Desktop\wb-analysis\data\cleaned\tn_merged.csv")

print(f"Total rows: {len(df)}")
print(f"\nNull 2021 winner: {df['Winner_Party_2021'].isna().sum()}")
print(f"Null 2021 votes: {df['Winner_Votes_2021'].isna().sum()}")
print(f"\nSeat Status:\n{df['Seat_Status'].value_counts()}")
print(f"\nTop parties 2026:\n{df['Winner_Party_2026'].value_counts().head(6)}")
print(f"\nTop parties 2021:\n{df['Winner_Party_2021'].value_counts().head(6)}")