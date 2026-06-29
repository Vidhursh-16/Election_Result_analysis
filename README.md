<div align="center">

# 🗳️ Election Result Intelligence Platform

### *Constituency-level political analytics for India's 2026 Assembly Elections*

[![Streamlit](https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://vidhursh-16-election-result-analysis-app-9s7hwx.streamlit.app/)
[![GitHub](https://img.shields.io/badge/Source-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Vidhursh-16/Election_Result_analysis)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge)](https://streamlit.io)

---

> **"A party that didn't exist in 2021 won Tamil Nadu in 2026.**
> **A party that ruled Bengal for 15 years lost in one election.**
> **This platform tells you exactly why — constituency by constituency."**

---

</div>

## 📌 What is this?

An interactive data journalism platform built during a **Digital Media internship at THG Publishing Pvt. Ltd. (The Hindu Group), Chennai**.

Click any of the **528 constituencies** across West Bengal and Tamil Nadu — and the platform tells you:
- Who won, who lost, and by how much
- Whether the seat flipped or was retained
- How it compares to 2021
- The demographic story behind the result

---

## 🗺️ States Covered

| State | Constituencies | Majority Mark | The Story |
|---|---|---|---|
| 🟧 **West Bengal** | 294 | 148 | TMC collapsed from 215 → 80 seats. BJP swept 9 complete districts. |
| 🟥 **Tamil Nadu** | 234 | 118 | TVK — founded in 2024 — won 207 seats in their **debut election**. |

---

## ✨ Features

### 🗺️ Interactive Choropleth Map
Click any constituency. Hover to see the winner. Toggle between **Political View** and **Intelligence View**.

### 📊 Party Intelligence Panels
Real-time computed stats — seats won, vote share, strongest region, top district, average victory margin.

### 🔍 Constituency Intelligence (Click Feature)
Three-column breakdown on click:
- **Overview** — Winner, Runner Up, Margin, Seat Status, SIR Risk
- **Political Summary** — Auto-generated narrative on why the seat flipped or was retained
- **2021 vs 2026 Comparison** — Vote share bars + margin change indicator

### 🧠 Election Intelligence Assistant
Ask anything. Type a constituency name — get a structured political summary with vote swing data.

### 🔀 State Switcher
Toggle between West Bengal and Tamil Nadu from the sidebar.

---

## 🔬 Key Findings

### West Bengal — Why TMC Lost
- **~91 lakh voters deleted** via SIR (Special Intensive Revision). In several seats, deletion count exceeded BJP's winning margin.
- **Teacher Recruitment Scam** drove educated urban voters away from TMC.
- BJP swept districts: Purba Medinipur, Purulia, Bankura, Jhargram, Paschim Bardhaman.
- TMC survived **only** in minority-dominant belts — Murshidabad, Malda, South 24 Parganas.

### Tamil Nadu — TVK's Historic Debut
- TVK founded **February 2024** → Won **207/234 seats** in 2026.
- DMK lost to anti-incumbency. AIADMK split the opposition vote.
- TVK's orange wave was strongest in **Chennai, North TN, and Central TN**.

---

## 🛠️ Tech Stack

```
Scraping     →  Python · pandas.read_html() · requests · BeautifulSoup
Processing   →  pandas · geopandas · numpy
GIS          →  Folium · KML → GeoJSON · Geometry Simplification
Frontend     →  Streamlit · streamlit-folium · HTML/CSS
Deployment   →  GitHub + Streamlit Cloud (CI/CD auto-deploy on push)
```

---

## 📂 Project Structure

```
wb-analysis/
├── app.py                          ← Entry point
├── engine/
│   ├── analytics_engine.py         ← Party & constituency stats
│   ├── assistant_engine.py         ← NLP query handler
│   ├── data_loader.py              ← GeoJSON loader with cache
│   └── story_engine.py             ← Auto narrative generator
├── ui/
│   ├── home.py                     ← West Bengal view
│   ├── home_tn.py                  ← Tamil Nadu view
│   └── components.py               ← Party panel component
├── data/
│   ├── raw/                        ← Scraped CSVs
│   ├── cleaned/                    ← Merged & enriched datasets
│   └── spatial/                    ← GeoJSON boundary files
└── dev/scripts/                    ← Data pipeline scripts
    ├── scrape.py
    ├── clean_tn.py
    ├── merge_geometry_tn.py
    └── simplify_geojson.py
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/Vidhursh-16/Election_Result_analysis.git
cd Election_Result_analysis
pip install -r requirements.txt
streamlit run app.py
```

---

## 📦 Requirements

```
streamlit
geopandas
folium
streamlit-folium
pandas
requests
pillow
```

---

## 🏛️ Built During

**Internship at THG Publishing Pvt. Ltd. (The Hindu Group)**
Digital Media Department · Chennai · June 2026

> *Mentor: Vinu Kirethey, Digital Media*
> *Built by: Vidhursh Kumar V, B.Tech AI & Data Science, Rajalakshmi Engineering College*

---

<div align="center">

**If this helped you — drop a ⭐ on the repo**

*Data sources: ECI · Wikipedia · Kaggle · Census 2011 · PLFS · Datameet India*

</div>
