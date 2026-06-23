from PIL import Image
import streamlit as st
import folium
from ui.components import party_panel
from streamlit_folium import st_folium
from engine.analytics_engine import get_party_summary
from folium.features import GeoJsonTooltip


def render_home(gdf):
    st.markdown("""<style>
.block-container { padding-top: 1rem; padding-bottom: 0rem; }
[data-testid="stMetricValue"] { font-size: 1.4rem; }
[data-testid="stMetric"] { padding: 0.2rem 0; }
div[data-testid="stVerticalBlock"] > div { gap: 0.3rem; }
</style>""", unsafe_allow_html=True)

    bjp_stats = get_party_summary(gdf, "BJP")
    aitc_stats = get_party_summary(gdf, "AITC")

    st.title("🗳️ West Bengal Election Intelligence Platform")
    st.caption("Political View • Story Mode • AI Analyst")

    left_col, center_col, right_col = st.columns([1.8, 5, 1.8])

    # ── LEFT PANEL — BJP ──────────────────────────
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

    # ── CENTER PANEL — MAP ────────────────────────
    with center_col:
        st.markdown("### Election Map")

        st.markdown("🟧 BJP &nbsp;&nbsp; 🟩 AITC &nbsp;&nbsp; ⬜ Others")

        view_mode = st.toggle("Intelligence View", value=False)

        if view_mode:
            st.info("Intelligence View Enabled")
        else:
            st.success("Political View Enabled")

        m = folium.Map(location=[23.5, 87.5], zoom_start=7, tiles="CartoDB positron")

        m.fit_bounds([
            [gdf.total_bounds[1], gdf.total_bounds[0]],
            [gdf.total_bounds[3], gdf.total_bounds[2]]
        ])

        def style_function(feature):
            party = feature["properties"].get("Winner_Party_2026", "")
            if party == "BJP":
                fill_color = "orange"
            elif party == "AITC":
                fill_color = "green"
            else:
                fill_color = "lightgray"
            return {"fillColor": fill_color, "color": "black", "weight": 0.5, "fillOpacity": 0.7}

        def intelligence_style(feature):
            return {"fillColor": "#000000", "color": "#444444", "weight": 0.7, "fillOpacity": 0.25}

        def highlight_function(feature):
            party = feature["properties"].get("Winner_Party_2026", "")
            if party == "BJP":
                color = "orange"
            elif party == "AITC":
                color = "green"
            else:
                color = "lightgray"
            return {"fillColor": color, "color": color, "weight": 3, "fillOpacity": 0.9}

        political_tooltip = GeoJsonTooltip(
            fields=["Constituency_Name", "Winner_Party_2026"],
            aliases=["Constituency:", "Winner:"],
            sticky=False, labels=True
        )

        intelligence_tooltip = GeoJsonTooltip(
            fields=["Constituency_Name", "District", "Region", "Winner_Party_2026",
                    "Vote_Swing", "Minority_Pct", "Women_Voter_Pct", "SIR_Risk"],
            aliases=["Constituency:", "District:", "Region:", "Winner:",
                     "Vote Swing:", "Minority %", "Women %", "Risk:"],
            sticky=False, labels=True
        )

        if view_mode:
            folium.GeoJson(gdf, name="Intelligence View", style_function=intelligence_style,
                            highlight_function=highlight_function, tooltip=intelligence_tooltip).add_to(m)
        else:
            folium.GeoJson(gdf, name="Political View", style_function=style_function,
                            tooltip=political_tooltip).add_to(m)

        st_folium(m, width=None, height=600, returned_objects=[])

        st.info("Click on a constituency to see detailed insights  \nUse toggle to switch between Political and Intelligence View")

    # ── RIGHT PANEL — AITC ────────────────────────
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

    # ── BOTTOM STATS BAR ──────────────────────────
    st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🏛 Total Constituencies", "294")
    c2.metric("🤝 Majority Mark", "148")
    c3.metric("📅 Election Year", "2026")
    c4.metric("🕒 Last Updated", "May 17, 2025")
    c5.metric("🔄 Data Source", "Compiled Dataset")