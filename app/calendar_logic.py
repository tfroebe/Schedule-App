from datetime import datetime
from collections import defaultdict

# ----------------------------
# 1️⃣ Helper functions
# ----------------------------

def time_to_minutes(time_str):
    """Convert 'HH:MM AM/PM' to minutes since midnight."""
    dt = datetime.strptime(time_str, "%I:%M %p")
    return dt.hour * 60 + dt.minute

def minutes_to_hhmm(minutes):
    """Convert minutes since midnight to 'HH:MM'."""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}:00"

# ----------------------------
# 2️⃣ Compute calendar with overlap counts
# ----------------------------

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
DAY_START = 8 * 60    # 08:00 AM
DAY_END = 20 * 60     # 08:00 PM
SLICE = 5             # 5-minute granularity
MAX_OVERLAP = 5       # Cap for overlap intensity

def compute_calendar(all_schedules):
    """
    Returns:
    busy: {
      day: [(start, end, overlap_count, user_id), ...]
    }
    """

    # day -> time -> set(user_ids)
    timeline = {
        day: defaultdict(set)
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    }

    # Build timeline
    for user_schedule in all_schedules:
        for event in user_schedule:
            for minute in range(event["start"], event["end"]):
                timeline[event["day"]][minute].add(event["user_id"])

    busy = {day: [] for day in timeline}

    # Collapse minutes into blocks
    for day, minutes in timeline.items():
        sorted_minutes = sorted(minutes.keys())
        if not sorted_minutes:
            continue

        start = sorted_minutes[0]
        current_users = minutes[start]

        prev = start

        for m in sorted_minutes[1:]:
            if m == prev + 1 and minutes[m] == current_users:
                prev = m
                continue

            busy[day].append((
                start,
                prev + 1,
                len(current_users),
                list(current_users)[0]  # user_id used for filtering
            ))

            start = m
            current_users = minutes[m]
            prev = m

        busy[day].append((
            start,
            prev + 1,
            len(current_users),
            list(current_users)[0]
        ))

    return {"busy": busy}