import pandas as pd
import streamlit as st

st.set_page_config(page_title="Competitor and Regulatory Intelligence Tracker", layout="wide")

st.title("Competitor and Regulatory Intelligence Tracker")
st.caption("Track market moves, regulatory updates, source quality and business implications.")

with st.sidebar:
    st.header("Digest Settings")
    audience = st.selectbox("Audience", ["Consulting manager", "Client leadership", "Strategy team", "Compliance lead"])
    market = st.text_input("Market / sector", "UK premium packaged food")
    week = st.text_input("Digest period", "Week of review")
    min_priority = st.slider("Show priority score at or above", 1, 5, 3)

sample = pd.DataFrame(
    {
        "Category": ["Competitor", "Regulatory", "Regulatory", "Customer"],
        "Topic": ["Competitor launch", "Labeling update", "Import requirement", "Premium demand signal"],
        "Source": ["Company announcement", "Regulator page", "Trade guidance", "Industry article"],
        "Source date": ["2026-07-01", "2026-07-03", "2026-07-04", "2026-07-05"],
        "Source link": [
            "https://example.com/company-announcement",
            "https://example.com/regulator-page",
            "https://example.com/trade-guidance",
            "https://example.com/industry-article",
        ],
        "Impact": ["Medium", "High", "High", "Medium"],
        "Urgency": ["Medium", "High", "High", "Low"],
        "Business implication": [
            "Review pricing and positioning",
            "Update compliance checklist",
            "Confirm customs documentation",
            "Validate customer segment and willingness to pay",
        ],
        "Recommended action": ["Monitor", "Escalate", "Validate", "Research further"],
        "Owner": ["Strategy", "Compliance", "Operations", "Research"],
    }
)

st.subheader("Intelligence Tracker")
edited = st.data_editor(sample, use_container_width=True, num_rows="dynamic", hide_index=True)

score_map = {"Low": 1, "Medium": 3, "High": 5}
edited["Impact score"] = edited["Impact"].map(score_map).fillna(1)
edited["Urgency score"] = edited["Urgency"].map(score_map).fillna(1)
edited["Priority score"] = ((edited["Impact score"] + edited["Urgency score"]) / 2).round(1)

priority_items = edited[edited["Priority score"] >= min_priority].sort_values(
    by="Priority score", ascending=False
)

st.subheader("Priority Flags")
col1, col2, col3 = st.columns(3)
col1.metric("Tracked items", len(edited))
col2.metric("Priority items", len(priority_items))
col3.metric("Highest priority", priority_items["Priority score"].max() if len(priority_items) else 0)

st.dataframe(
    priority_items[
        [
            "Category",
            "Topic",
            "Impact",
            "Urgency",
            "Priority score",
            "Business implication",
            "Recommended action",
            "Owner",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Weekly Digest")
if priority_items.empty:
    st.write("No items meet the selected priority threshold.")
else:
    for _, row in priority_items.iterrows():
        st.markdown(
            f"- **{row['Topic']}** ({row['Category']}, priority {row['Priority score']}/5): "
            f"{row['Business implication']} - {row['Recommended action']} ({row['Owner']})."
        )

st.subheader("Management Summary")
regulatory_count = len(priority_items[priority_items["Category"].str.lower() == "regulatory"])
competitor_count = len(priority_items[priority_items["Category"].str.lower() == "competitor"])

if regulatory_count > competitor_count:
    summary = "Regulatory updates are the strongest current signal. The team should validate compliance requirements before commercial commitments."
elif competitor_count > regulatory_count:
    summary = "Competitor activity is the strongest current signal. The team should review positioning, pricing and differentiation."
else:
    summary = "The current intelligence set is balanced. The team should monitor both commercial and regulatory signals before the next decision."

st.write(summary)

digest = f"""# Competitor and Regulatory Intelligence Digest

## Audience
{audience}

## Market / Sector
{market}

## Period
{week}

## Management Summary
{summary}

## Priority Items
{chr(10).join("- " + row["Topic"] + " (" + row["Category"] + ", priority " + str(row["Priority score"]) + "/5): " + row["Business implication"] + " - " + row["Recommended action"] + " [" + row["Owner"] + "]" for _, row in priority_items.iterrows()) or "No priority items above threshold."}

## Source Register
{chr(10).join("- " + row["Topic"] + ": " + row["Source"] + " | " + row["Source date"] + " | " + row["Source link"] for _, row in edited.iterrows())}

## Responsible Use Note
Treat unsourced items as assumptions. Validate source dates and links before using this digest for client or leadership decisions.
"""

st.download_button(
    "Download Intelligence Digest",
    data=digest,
    file_name="competitor_regulatory_intelligence_digest.md",
    mime="text/markdown",
)
