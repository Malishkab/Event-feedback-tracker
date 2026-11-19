import pandas as pd
import streamlit as st

st.set_page_config(page_title="Event Feedback Tracker", layout="wide")
st.title("Event Feedback and Follow-up Tracker")
st.caption("Uses generated sample data for demonstration.")
import plotly.express as px

full_df = pd.read_csv("feedback.csv")
df = full_df.copy()
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.strftime("%Y-%m")
# Sidebar filter
event_choice = st.sidebar.selectbox("Choose an event", ["All"] + sorted(df["event"].unique()))
if event_choice != "All":
    df = df[df["event"] == event_choice]

# Key numbers
col1, col2, col3 = st.columns(3)
col1.metric("Responses", len(df))
col2.metric("Average rating", round(df["rating"].mean(), 2))
col3.metric("Pending follow-ups", (df["follow_up_status"] == "Pending").sum())

st.dataframe(df)

st.subheader("Ratings overview")
left, right = st.columns(2)

# Chart 1: average rating per event (uses ALL data so events can be compared)
event_avg = full_df.groupby("event")["rating"].mean().round(2)
left.plotly_chart(px.bar(event_avg, title="Average rating by event",
                         labels={"value": "Average rating", "event": "Event"}),
                  use_container_width=True)

# Chart 2: how many 1-star, 2-star... ratings (uses the filtered data)
dist = df["rating"].value_counts().sort_index()
right.plotly_chart(px.bar(dist, title="Rating distribution",
                          labels={"value": "Responses", "rating": "Rating"}),
                   use_container_width=True)

# Auto-written insight
st.info(f"Highest rated event: {event_avg.idxmax()} ({event_avg.max()}). "
        f"Lowest rated event: {event_avg.idxmin()} ({event_avg.min()}).")

st.subheader("What are people saying?")

themes = {
    "Venue / space": ["venue", "crowded"],
    "Timing": ["late", "too little time"],
    "Audio / tech": ["sound"],
    "Registration": ["registration", "confusing"],
    "Content quality": ["informative", "useful", "learned", "content"],
    "Engagement": ["hands-on", "engaging", "speakers"],
    "Organization": ["organized", "smooth", "friendly"],
}

def count_themes(comments):
    counts = {}
    for theme, words in themes.items():
        counts[theme] = sum(any(w in c.lower() for w in words) for c in comments)
    return pd.Series(counts)

complaints = count_themes(df[df["rating"] <= 2]["comment"])
praise = count_themes(df[df["rating"] >= 4]["comment"])

a, b = st.columns(2)
a.plotly_chart(px.bar(complaints[complaints > 0], title="Top complaint themes (ratings 1-2)",
                      labels={"value": "Mentions", "index": "Theme"}), use_container_width=True)
b.plotly_chart(px.bar(praise[praise > 0], title="Top praise themes (ratings 4-5)",
                      labels={"value": "Mentions", "index": "Theme"}), use_container_width=True)
trend = df.groupby("month")["rating"].mean().round(2)
st.plotly_chart(px.line(trend, markers=True, title="Average rating over time",
                        labels={"value": "Average rating", "month": "Month"}),
                use_container_width=True)
st.subheader("Follow-up tracker")

statuses = ["Pending", "Done", "Not needed"]
chosen = st.multiselect("Show status", statuses, default=["Pending"])

urgent = ((df["rating"] <= 2) & (df["follow_up_status"] == "Pending")).sum()
st.warning(f"{urgent} unhappy attendees are still waiting for a follow-up.")

cols = ["attendee_id", "name", "event", "rating", "comment", "follow_up_status"]
to_edit = df[df["follow_up_status"].isin(chosen)][cols]

edited = st.data_editor(
    to_edit,
    disabled=["attendee_id", "name", "event", "rating", "comment"],
    column_config={"follow_up_status": st.column_config.SelectboxColumn(
        "follow_up_status", options=statuses)},
    key="editor",
)

if st.button("Save changes"):
    full_df.loc[edited.index, "follow_up_status"] = edited["follow_up_status"]
    full_df.to_csv("feedback.csv", index=False)
    st.success("Saved!")
    st.rerun()

st.download_button("Download this list as CSV",
                   edited.to_csv(index=False), "follow_ups.csv", "text/csv")

with st.expander("See all raw data"):
    st.dataframe(df)