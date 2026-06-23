from PIL import Image
import streamlit as st
import folium
from ui.components import party_panel
from streamlit_folium import st_folium
from engine.analytics_engine import get_party_summary
from folium.features import GeoJsonTooltip
from engine.assistant_engine import answer_query


def render_home_tn(gdf):
    st.markdown("""<style>
.block-container { padding-top: 1rem; padding-bottom: 0rem; }
[data-testid="stMetricValue"] { font-size: 1.4rem; }
[data-testid="stMetric"] { padding: 0.2rem 0; }
div[data-testid="stVerticalBlock"] > div { gap: 0.3rem; }
</style>""", unsafe_allow_html=True)

    tvk_stats = get_party_summary(gdf, "TVK")
    dmk_stats = get_party_summary(gdf, "DMK")

    st.title("🗳️ Tamil Nadu Election Intelligence Platform")

    left_col, center_col, right_col = st.columns([1.8, 5, 1.8])

    with left_col:
        party_panel(
            leader_name="Vijay",
            leader_photo="ui/views/vijay.jpeg",
            party_name="🟧 TVK",
            party_short="TVK",
            seats=tvk_stats["seats"],
            vote_share=tvk_stats["vote_share"],
            strongest_region=tvk_stats["strongest_region"],
            top_district=tvk_stats["top_district"],
            avg_margin=tvk_stats["average_margin"],
            color="#FF6600",
        )

    with center_col:
        st.markdown("### Election Map")

        view_mode = st.toggle("Intelligence View", value=False)

        status = "✅ Political View Enabled" if not view_mode else "🔍 Intelligence View Enabled"
        st.markdown(f"🟧 TVK &nbsp; 🟥 DMK &nbsp; 🟩 AIADMK &nbsp; ⬜ Others &nbsp;&nbsp;|&nbsp;&nbsp; {status}")

        m = folium.Map(location=[11.1, 78.6], zoom_start=7, tiles="CartoDB positron")
        m.fit_bounds([
            [gdf.total_bounds[1], gdf.total_bounds[0]],
            [gdf.total_bounds[3], gdf.total_bounds[2]]
        ])

        def style_function(feature):
            party = feature["properties"].get("Winner_Party_2026", "")
            if party == "TVK": fill_color = "orange"
            elif party == "DMK": fill_color = "red"
            elif party in ["ADMK", "AIADMK"]: fill_color = "green"
            else: fill_color = "lightgray"
            return {"fillColor": fill_color, "color": "black", "weight": 0.5, "fillOpacity": 0.7}

        def intelligence_style(feature):
            return {"fillColor": "#000000", "color": "#444444", "weight": 0.7, "fillOpacity": 0.25}

        def highlight_function(feature):
            party = feature["properties"].get("Winner_Party_2026", "")
            if party == "TVK": color = "orange"
            elif party == "DMK": color = "red"
            elif party in ["ADMK", "AIADMK"]: color = "green"
            else: color = "lightgray"
            return {"fillColor": color, "color": color, "weight": 3, "fillOpacity": 0.9}

        political_tooltip = GeoJsonTooltip(
            fields=["Constituency_Name_x", "Winner_Party_2026"],
            aliases=["Constituency:", "Winner:"],
            sticky=False, labels=True
            )

        intelligence_tooltip = GeoJsonTooltip(
            fields=["Constituency_Name_x", "District", "Region", "Winner_Party_2026",
            "Vote_Swing", "Minority_Pct", "Women_Voter_Pct", "SIR_Risk"],
            aliases=["Constituency:", "District:", "Region:", "Winner:","Vote Swing:", "Minority %", "Women %", "Risk:"],
            sticky=False, labels=True
            )

        if view_mode:
            folium.GeoJson(gdf, name="Intelligence View", style_function=intelligence_style,
                           highlight_function=highlight_function, tooltip=intelligence_tooltip).add_to(m)
        else:
            folium.GeoJson(gdf, name="Political View", style_function=style_function,
                           tooltip=political_tooltip).add_to(m)

        map_data = st_folium(
            m, width=None, height=500,
            returned_objects=["last_active_drawing", "last_object_clicked_tooltip"]
        )

        st.caption("Click on a constituency for details • Toggle for Intelligence View")

    with right_col:
        party_panel(
            leader_name="M.K. Stalin",
            leader_photo="ui/views/stalin.jpeg",
            party_name="🟥 DMK",
            party_short="DMK",
            seats=dmk_stats["seats"],
            vote_share=dmk_stats["vote_share"],
            strongest_region=dmk_stats["strongest_region"],
            top_district=dmk_stats["top_district"],
            avg_margin=dmk_stats["average_margin"],
            color="#CC0000",
        )

    # ── PHASE 4 — CONSTITUENCY INTELLIGENCE ──────────
    props = None

    if map_data and map_data.get("last_active_drawing"):
        props = map_data["last_active_drawing"].get("properties", {})

    if props:
        st.markdown("---")
        st.markdown(f"### 📍 {props.get('Constituency_Name_x', 'N/A')}")
        st.caption("Constituency Overview")

        col_a, col_b, col_c = st.columns([1.5, 2, 2])

        with col_a:
            winner = props.get("Winner_Party_2026", "N/A")
            party_change = props.get("Party_Change", "→")
            runner = party_change.split("→")[0].strip() if "→" in party_change else "N/A"

            st.markdown(f"""
| Field | Value |
|---|---|
| **Winner (2026)** | {winner} |
| **Runner Up** | {runner} |
| **Victory Margin** | {props.get('Margin_2026', 'N/A'):,} |
| **Region** | {props.get('Region', 'N/A')} |
| **District** | {props.get('District', 'N/A')} |
| **Seat Status** | {props.get('Seat_Status', 'N/A')} |
| **SIR Risk** | {props.get('SIR_Risk', 'N/A')} |
""", unsafe_allow_html=True)

        with col_b:
            seat_status = props.get("Seat_Status", "")
            swing = props.get("Vote_Swing", 0)
            margin_change = props.get("Margin_Change", 0)
            region = props.get("Region", "this region")

            if seat_status == "Flipped":
                summary = f"{winner} flipped this constituency from {runner}, marking a significant shift in {region}."
            else:
                summary = f"{winner} retained this constituency, continuing their dominance in {region}."

            if margin_change > 0:
                trend = f"The winning margin increased by {abs(margin_change):,} votes compared to 2021."
            elif margin_change < 0:
                trend = f"The winning margin decreased by {abs(margin_change):,} votes from 2021."
            else:
                trend = "The margin remained stable compared to 2021."

            st.markdown(f"""
<div style='background:#1a1a2e; padding:1rem; border-radius:8px; border-left:3px solid #FF6600;'>
<b>🏛 Political Summary</b><br><br>{summary}<br><br>{trend}
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div style='background:#1a1a2e; padding:1rem; border-radius:8px; border-left:3px solid #CC0000; margin-top:0.5rem;'>
<b>💡 Key Insight</b><br><br>
Vote swing of <b>{swing:+.2f}%</b> with SIR Risk rated <b>{props.get('SIR_Risk','N/A')}</b>.
Minority population at <b>{props.get('Minority_Pct','N/A')}%</b>,
Women voters at <b>{props.get('Women_Voter_Pct','N/A')}%</b>.
</div>
""", unsafe_allow_html=True)

        with col_c:
            st.markdown("### 📊 Election Comparison")

            pct_2021 = props.get("Winner_Pct_2021", 0)
            pct_2026 = props.get("Winner_Pct_2026", 0)
            winner_2021 = props.get("Winner_Party_2021", "N/A")

            st.markdown(f"""
<div style='margin-bottom:0.8rem;'>
<span>2021 — {winner_2021}</span>
<div style='background:#333; border-radius:4px; height:18px; width:100%;'>
<div style='background:#CC0000; width:{pct_2021}%; height:18px; border-radius:4px;'></div>
</div>
<b>{pct_2021:.2f}%</b>
</div>
<div style='margin-bottom:0.8rem;'>
<span>2026 — {winner}</span>
<div style='background:#333; border-radius:4px; height:18px; width:100%;'>
<div style='background:#FF6600; width:{pct_2026}%; height:18px; border-radius:4px;'></div>
</div>
<b>{pct_2026:.2f}%</b>
</div>
""", unsafe_allow_html=True)

            mc_color = "#2ECC71" if margin_change >= 0 else "#E74C3C"
            st.markdown(f"""
<h2 style='color:{mc_color};'>{margin_change:+,}</h2>
<span style='color:gray;'>votes change from 2021</span>
""", unsafe_allow_html=True)

    # ── ASSISTANT ─────────────────────────────────
    st.markdown("---")
    st.subheader("🧠 Election Intelligence Assistant")
    question = st.text_input("Ask about the election", placeholder="Example: Explain Chennai North")
    if st.button("Ask"):
        if question.strip():
            response = answer_query(question, gdf)
            st.markdown(response)

    # ── BOTTOM STATS BAR ──────────────────────────
    st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🏛 Total Constituencies", "234")
    c2.metric("🤝 Majority Mark", "118")
    c3.metric("📅 Election Year", "2026")
    c4.metric("🕒 Last Updated", "Jun 2026")
    c5.metric("🔄 Data Source", "Compiled Dataset")