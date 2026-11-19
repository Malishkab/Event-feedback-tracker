# Event-feedback-tracker

A small web dashboard that helps event teams turn raw attendee feedback into clear insights and keep track of who still needs a follow-up.

Why I built it?
Event teams often collect feedback through forms but rarely analyze it properly, and follow-ups with unhappy attendees can get forgotten. This tool puts the analysis and the follow-up list in one place so a team can see what went well, what to fix, and who still needs a reply.

Features
Key numbers at a glance: total responses, average rating, and pending follow-ups
Event comparison: average rating for each event, with an automatic summary of the best and lowest rated event
Rating distribution and rating trend over time
Comment theme analysis: keyword-based counting of themes (venue, timing, audio, registration, content, engagement, organization), split into complaint themes (ratings 1-2) and praise themes (ratings 4-5)
Follow-up tracker: an editable table to update each attendee's status (Pending, Done, Not needed), with a warning showing how many unhappy attendees are still waiting
Export: download the filtered follow-up list as a CSV file
Event filter in the sidebar to focus on a single event

Tech stack
Python, Pandas, Streamlit, Plotly
