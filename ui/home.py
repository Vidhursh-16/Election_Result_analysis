from PIL import GimpGradientFile
from PIL import Image
import streamlit as st
import folium
from ui.components import party_panel
from streamlit_folium import st_folium
from engine.analytics_engine import get_party_summary
from folium.features import GeoJsonTooltip
from engine.assistant_engine import answer_query

def render_home(gdf):
    st.markdown("""
<style>
.block-container { padding-top: 1rem; padding-bottom: 0rem; }
[data-testid="stMetricValue"] { font-size: 1.4rem; }
[data-testid="stMetric"] { padding: 0.2rem 0; }
div[data-testid="stVerticalBlock"] > div { gap: 0.3rem; }
</style>
""", unsafe_allow_html=True)

    bjp_stats = get_party_summary(gdf, "BJP")
    aitc_stats = get_party_summary(gdf, "AITC")

    st.title("🗳️ West Bengal Election Intelligence Platform")

    left_col, center_col, right_col = st.columns([1.8, 5, 1.8])

    with left_col:
        party_panel(
            leader_name="Narendra Modi",
            leader_photo="ui/views/modi.jpeg",
            party_name="🟧 BJP",
            party_short="BJP",
            seats=bjp_stats["seats"],
            vote_share=bjp_stats["vote_share"],
            strongest_region=bjp_stats["strongest_region"],
            top_district=bjp_stats["top_district"],
            avg_margin=bjp_stats["average_margin"],
            color="#F57C00",
        )

    with center_col:
        st.markdown("### Election Map")

        st.markdown("🟧 BJP &nbsp; 🟩 AITC &nbsp; ⬜ Others")

        m = folium.Map(location=[23.5, 87.5], zoom_start=7, tiles="CartoDB positron")
        m.fit_bounds([
            [gdf.total_bounds[1], gdf.total_bounds[0]],
            [gdf.total_bounds[3], gdf.total_bounds[2]]
        ])

        def style_function(feature):
            party = feature["properties"].get("Winner_Party_2026", "")
            if party == "BJP": fill_color = "orange"
            elif party == "AITC": fill_color = "green"
            else: fill_color = "lightgray"
            return {"fillColor": fill_color, "color": "black", "weight": 0.5, "fillOpacity": 0.7}


        political_tooltip = GeoJsonTooltip(
            fields=["Constituency_Name", "Winner_Party_2026"],
            aliases=["Constituency:", "Winner:"],
            sticky=False, labels=True
        )
        folium.GeoJson(
            gdf,
            name="Political View",
            style_function=style_function,
            tooltip=political_tooltip
            ).add_to(m)
        map_data = st_folium(
            m, width=None, height=500,
            returned_objects=["last_active_drawing"]
        )

    with right_col:
        party_panel(
            leader_name="Mamata Banerjee",
            leader_photo="ui/views/mamta.jpeg",
            party_name="🟩 AITC",
            party_short="AITC",
            seats=aitc_stats["seats"],
            vote_share=aitc_stats["vote_share"],
            strongest_region=aitc_stats["strongest_region"],
            top_district=aitc_stats["top_district"],
            avg_margin=aitc_stats["average_margin"],
            color="#2E7D32",
        )

    # ── PHASE 4 — CONSTITUENCY INTELLIGENCE ──────────
    props = None

    if map_data and map_data.get("last_active_drawing"):
        props = map_data["last_active_drawing"].get("properties", {})

    if props:
        st.markdown("---")
        st.markdown(f"### 📍 {props.get('Constituency_Name', 'N/A')}")
        st.caption("Constituency Overview")

        col_a, col_b, col_c = st.columns([1.5, 2, 2])

        with col_a:
            winner = props.get("Winner_Party_2026", "N/A")
            party_change = props.get("Party_Change", "→")
            runner = party_change.split("→")[0].strip() if "→" in party_change else "N/A"
            winner_color = "#F57C00" if winner == "BJP" else "#2E7D32"
            runner_color = "#2E7D32" if runner == "AITC" else "#F57C00"

            st.markdown(f"""
| Field | Value |
|---|---|
| **Winner (2026)** | <span style='color:{winner_color}'>{winner}</span> |
| **Runner Up** | <span style='color:{runner_color}'>{runner}</span> |
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
                trend = f"The winning margin increased by {abs(margin_change):,} votes compared to 2021 — showing strengthened support."
            elif margin_change < 0:
                trend = f"The winning margin decreased by {abs(margin_change):,} votes from 2021 — indicating a tighter contest."
            else:
                trend = "The margin remained stable compared to 2021."

            st.markdown(f"""
<div style='background:#1a1a2e; padding:1rem; border-radius:8px; border-left:3px solid #F57C00;'>
<b>🏛 Political Summary</b><br><br>{summary}<br><br>{trend}
</div>
""", unsafe_allow_html=True)

            insight_color = "#F57C00" if winner == "BJP" else "#2E7D32"
            st.markdown(f"""
<div style='background:#1a1a2e; padding:1rem; border-radius:8px; border-left:3px solid {insight_color}; margin-top:0.5rem;'>
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
         bar_color_2021 = "#F57C00" if winner_2021 == "BJP" else "#2E7D32"
         bar_color_2026 = "#F57C00" if winner == "BJP" else "#2E7D32"

         st.markdown(f"""<div style='margin-bottom:0.8rem;'><b>2021 — {winner_2021}</b><div style='background:#333;border-radius:4px;height:18px;width:100%;'><div style='background:{bar_color_2021};width:{pct_2021}%;height:18px;border-radius:4px;'></div>
         </div><span style='color:{bar_color_2021};'><b>{pct_2021:.2f}%</b></span></div>""",unsafe_allow_html=True)

         st.markdown( f"""<div style='margin-bottom:1rem;'><b>2026 — {winner}</b><div style='background:#333;border-radius:4px;height:18px;width:100%;'><div style='background:{bar_color_2026};width:{pct_2026}%;height:18px;border-radius:4px;'></div></div><span style='color:{bar_color_2026};'><b>{pct_2026:.2f}%</b></span></div>""",
         unsafe_allow_html=True,
         )
         mc_color = "#2ECC71" if margin_change >= 0 else "#E74C3C"
         if margin_change > 20000:
            trend_icon = "🟢"
            trend_title = "Stronger Mandate"
            trend_text = (
                f"The winning margin increased by "
                f"{margin_change:,} votes compared to 2021, "
                "indicating stronger electoral support."
            )
         elif margin_change > 0:
            trend_icon = "🟡"
            trend_title = "Improved Performance"
            trend_text = (
                f"The party improved its winning margin by "
                f"{margin_change:,} votes over the previous election."
            )

         else:
            trend_icon = "🔴"
            trend_title = "Major Political Shift"
            trend_text = (
                 f"The winning margin declined by "
                 f"{abs(margin_change):,} votes compared to 2021, "
                 "indicating a significant political change."
                )


        st.markdown(
        f"""
<div style="
background:#1a1a2e;
padding:1rem;
border-radius:8px;
border-left:4px solid {mc_color};
margin-top:0.8rem;">

<b>{trend_icon} Election Trend</b>

<h4 style="margin-top:8px;margin-bottom:10px;">
{trend_title}
</h4>

<p style="margin-bottom:0;">
{trend_text}
</p>

</div>
""",
        unsafe_allow_html=True,
    )
    # ── BOTTOM STATS BAR ──────────────────────────
    st.markdown("---")
    st.subheader("🧠 Election Intelligence Assistant")

    question = st.text_input(
        "Ask about the election",
        placeholder="Example: Explain Kalimpong"
    )

    if st.button("Ask"):
      if question.strip():
        response = answer_query(question, gdf)
        st.markdown(response)
        st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🏛 Total Constituencies", "294")
    c2.metric("🤝 Majority Mark", "148")
    c3.metric("📅 Election Year", "2026")
    c4.metric("🕒 Last Updated", "May 17, 2025")
    c5.metric("🔄 Data Source", "Compiled Dataset")