from datetime import datetime

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
    return f"{h:02d}:{m:02d}"

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
    - busy: dict {day: list of (start_minute, end_minute, overlap_count)}
    """
    busy_with_counts = {day: [] for day in DAYS}

    for day in DAYS:
        # Initialize timeline with 0s
        timeline = {t: 0 for t in range(DAY_START, DAY_END, SLICE)}

        # Count overlaps per time slice
        for user in all_schedules:
            for event in user:
                if event["day"] == day:
                    for t in range(event["start"], event["end"], SLICE):
                        if t in timeline:
                            timeline[t] += 1

        # Merge contiguous slices with same count
        merged = []
        current_start = None
        current_count = 0

        for t in range(DAY_START, DAY_END + SLICE, SLICE):
            count = timeline.get(t, 0)

            if count != current_count:
                if current_count > 0:
                    merged.append((
                        current_start,
                        t,
                        min(current_count, MAX_OVERLAP)  # Cap at 5
                    ))
                current_start = t
                current_count = count

        busy_with_counts[day] = merged

    return {"busy": busy_with_counts}
