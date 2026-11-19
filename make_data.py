import pandas as pd
import random

random.seed(42)  # makes the "random" data the same every time

events = ["Tech Talk", "Coding Workshop", "Career Panel",
          "Hackathon Kickoff", "Alumni Meet", "Resume Clinic"]

positive = ["Great speakers and very informative",
            "Well organized and engaging",
            "Loved the hands-on activities",
            "Very useful content, learned a lot",
            "Friendly team and smooth registration"]

negative = ["The venue was too crowded",
            "Event started late",
            "Sound quality was poor",
            "Too much content in too little time",
            "Registration process was confusing"]

neutral = ["It was okay overall",
           "Some parts were good, some were slow",
           "Decent event but could be better"]

rows = []
for i in range(150):
    rating = random.choice([1, 2, 3, 3, 4, 4, 4, 5, 5, 5])
    if rating >= 4:
        comment = random.choice(positive)
    elif rating == 3:
        comment = random.choice(neutral)
    else:
        comment = random.choice(negative)

    rows.append({
        "attendee_id": 1000 + i,
        "name": f"Attendee {i + 1}",
        "event": random.choice(events),
        "date": f"2026-{random.randint(1, 10):02d}-{random.randint(1, 28):02d}",
        "rating": rating,
        "comment": comment,
        "follow_up_status": random.choice(["Pending", "Done", "Not needed"]),
    })

pd.DataFrame(rows).to_csv("feedback.csv", index=False)
print("Created feedback.csv with", len(rows), "rows")