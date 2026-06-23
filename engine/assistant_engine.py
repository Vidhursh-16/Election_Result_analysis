"""
Election Intelligence Assistant

Version 1
---------
Receives a user question.
Identifies the intent.
Returns the detected intent.

No analytics.
No story generation.
No UI.
"""

from enum import Enum
from engine.analytics_engine import get_constituency
from engine.story_engine import generate_constituency_story

class Intent(Enum):
    CONSTITUENCY = "constituency"
    REGION = "region"
    DISTRICT = "district"
    HIGH_RISK = "high_risk"
    PARTY_CHANGE = "party_change"
    COMPETITIVE = "competitive"
    UNKNOWN = "unknown"


def detect_intent(question: str) -> Intent:
    """
    Detect the user's query intent using simple keyword matching.
    """

    q = question.lower().strip()

    if any(word in q for word in ["explain", "constituency"]):
        return Intent.CONSTITUENCY

    if "region" in q or "north bengal" in q:
        return Intent.REGION

    if "district" in q:
        return Intent.DISTRICT

    if "high risk" in q:
        return Intent.HIGH_RISK

    if "changed party" in q or "party change" in q or "flipped" in q:
        return Intent.PARTY_CHANGE

    if "competitive" in q or "close contest" in q:
        return Intent.COMPETITIVE

    return Intent.UNKNOWN


def answer_query(question: str, gdf):
    intent = detect_intent(question)

    if intent == Intent.CONSTITUENCY:
        constituency = question.upper()
        for word in ["EXPLAIN", "TELL ME ABOUT", "WHAT ABOUT", "CONSTITUENCY", "SHOW"]:
            constituency = constituency.replace(word, "")
        constituency = constituency.strip()

        col = "Constituency_Name_x" if "Constituency_Name_x" in gdf.columns else "Constituency_Name"

        # Exact match first
        exact = gdf[gdf[col].str.upper() == constituency]
        if not exact.empty:
            data = exact.iloc[0].to_dict()
        else:
            # Partial match
            partial = gdf[gdf[col].str.upper().str.contains(constituency, na=False)]
            if not partial.empty:
                data = partial.iloc[0].to_dict()
            else:
                return f"'{constituency}' not found. Type the constituency name as it appears on the map."

        name = data.get('Constituency_Name_x') or data.get('Constituency_Name', 'N/A')
        story = generate_constituency_story(data)

        return f"📍 **{name}**\n\n{story['summary']}\n\n{story['trend']}\n\nVote Swing: **{story['swing']:+.2f}%**"

    return "Try: 'Explain PONNERI' or 'Explain CHENNAI NORTH'"