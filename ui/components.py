import streamlit as st

def party_panel(
    leader_name,
    leader_photo,
    party_name,
    party_short,
    seats,
    vote_share,
    strongest_region,
    top_district,
    avg_margin,
    color,
):
    with st.container(border=True):
        st.markdown(
            f"<h3 style='color:{color};'>{party_name}</h3>",
            unsafe_allow_html=True
        )

        col_img, col_text = st.columns([1, 2])
        with col_img:
            st.image(leader_photo, width=500)
        with col_text:
            st.caption("LEADER")
            st.markdown(f"**{leader_name}**")

        st.divider()

        st.metric(label="🏛 Seats Won", value=f"{seats} of 294")
        st.metric(label="📊 Vote Share", value=vote_share)
        st.metric(label="📍 Strongest Region", value=strongest_region)
        st.metric(label="🏆 Top Performing District", value=top_district)
        st.metric(label="📈 Avg Victory Margin", value=f"{avg_margin} votes")