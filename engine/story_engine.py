def generate_constituency_story(props):

    winner = props.get("Winner_Party_2026", "N/A")

    party_change = props.get("Party_Change", "→")

    runner = (
        party_change.split("→")[0].strip()
        if "→" in party_change
        else "N/A"
    )

    seat_status = props.get("Seat_Status", "")
    region = props.get("Region", "this region")
    margin_change = props.get("Margin_Change", 0)
    swing = props.get("Vote_Swing", 0)

    if seat_status == "Flipped":
        summary = (
            f"{winner} flipped this constituency from "
            f"{runner}, marking a significant political shift in {region}."
        )
    else:
        summary = (
            f"{winner} retained this constituency, "
            f"continuing its dominance in {region}."
        )

    if margin_change > 0:
        trend = (
            f"The winning margin increased by "
            f"{abs(margin_change):,} votes compared to 2021."
        )
    elif margin_change < 0:
        trend = (
            f"The winning margin decreased by "
            f"{abs(margin_change):,} votes compared to 2021."
        )
    else:
        trend = "The winning margin remained stable."

    return {
        "summary": summary,
        "trend": trend,
        "swing": swing,
    }