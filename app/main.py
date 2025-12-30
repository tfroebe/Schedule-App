from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import calendar_logic
import pandas as pd
import io
from datetime import datetime, timedelta
import os
import logging

# ----------------------------
# Configuration
# ----------------------------

SEMESTER_START = datetime(2026, 1, 19)
SEMESTER_END = datetime(2026, 5, 13)

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Group Schedule API")

# ----------------------------
# Static files
# ----------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse(os.path.join("static", "index.html"))

# ----------------------------
# In-memory storage
# ----------------------------
# all_schedules = [
#   [
#     {user_id, username, day, start, end},
#     ...
#   ],
#   ...
# ]
all_schedules = []

# ----------------------------
# Helpers
# ----------------------------

def generate_weekly_dates(start_date, end_date, weekday):
    """Return all dates between start and end that fall on weekday."""
    dates = []
    current = start_date
    while current.weekday() != weekday:
        current += timedelta(days=1)

    while current <= end_date:
        dates.append(current)
        current += timedelta(weeks=1)

    return dates

# ----------------------------
# Upload CSV
# ----------------------------

@app.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    username: str = Form(...)
):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    user_id = len(all_schedules)
    user_schedule = []

    for _, row in df.iterrows():
        start_minutes = calendar_logic.time_to_minutes(row["Start Time"])
        end_minutes = calendar_logic.time_to_minutes(row["End Time"])
        start_date = datetime.strptime(row["Start Date"], "%m/%d/%Y")
        weekday = start_date.weekday()
        weekday_name = start_date.strftime("%A")

        weekly_dates = generate_weekly_dates(
            SEMESTER_START,
            SEMESTER_END,
            weekday
        )

        for _ in weekly_dates:
            user_schedule.append({
                "user_id": user_id,
                "username": username,
                "day": weekday_name,
                "start": start_minutes,
                "end": end_minutes
            })

    all_schedules.append(user_schedule)

    logging.info(f"Uploaded schedule for user {username} (id={user_id})")

    return {
        "status": "uploaded",
        "events_count": len(user_schedule),
        "user_id": user_id,
        "username": username
    }

# ----------------------------
# Calendar endpoint
# ----------------------------

@app.get("/calendar")
def get_calendar():
    if not all_schedules:
        return {"message": "No schedules uploaded yet."}

    calendar_data = calendar_logic.compute_calendar(all_schedules)

    # busy format:
    # { day: [(start_min, end_min, overlap_count, user_id), ...] }

    busy = {}

    for day, events in calendar_data["busy"].items():
        busy[day] = [
            [
                calendar_logic.minutes_to_hhmm(start),
                calendar_logic.minutes_to_hhmm(end),
                count,
                user_id
            ]
            for start, end, count, user_id in events
        ]

    return {"busy": busy}

# ----------------------------
# Reset
# ----------------------------

@app.post("/reset")
def reset_schedules():
    global all_schedules
    all_schedules = []
    logging.info("All schedules reset")
    return {"status": "reset"}