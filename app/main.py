from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import calendar_logic
import pandas as pd
import io
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Starting FastAPI app...")


app = FastAPI(title="Group Schedule API")

# ----------------------------
# 🔹 STATIC FILES SETUP
# ----------------------------

# Serve files from the "static" directory at /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root route to serve index.html
@app.get("/")
def read_index():
    return FileResponse(os.path.join("static", "index.html"))

# ----------------------------
# In-memory storage for all uploaded schedules
# ----------------------------
all_schedules = []

# ----------------------------
# 1️⃣ Upload endpoint
# ----------------------------
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a single user's schedule CSV
    CSV columns:
    Subject, Start Date, Start Time, End Date, End Time, Location, Description
    """
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    user_schedule = []

    for _, row in df.iterrows():
        start_minutes = calendar_logic.time_to_minutes(row["Start Time"])
        end_minutes = calendar_logic.time_to_minutes(row["End Time"])
        day = datetime.strptime(row["Start Date"], "%m/%d/%Y").strftime("%A")

        user_schedule.append({
            "subject": row["Subject"],
            "day": day,
            "start": start_minutes,
            "end": end_minutes
        })

    all_schedules.append(user_schedule)

    return {
        "status": "uploaded",
        "events_count": len(user_schedule)
    }

# ----------------------------
# 2️⃣ Calendar endpoint
# ----------------------------
@app.get("/calendar")
def get_calendar():
    """
    Returns merged calendar data for all uploaded users:
    - busy times with overlap count
    """
    if not all_schedules:
        return {"message": "No schedules uploaded yet."}

    calendar_data = calendar_logic.compute_calendar(all_schedules)

    # busy_with_counts format: {day: [(start_min, end_min, overlap_count), ...]}
    busy = {}

    for day, events in calendar_data["busy"].items():
        # convert start and end times to HH:MM string format
        busy[day] = [
            [
                calendar_logic.minutes_to_hhmm(start),
                calendar_logic.minutes_to_hhmm(end),
                count
            ]
            for start, end, count in events
        ]

    return {"busy": busy}

# ----------------------------
# 3️⃣ Reset endpoint
# ----------------------------
@app.post("/reset")
def reset_schedules():
    global all_schedules
    all_schedules = []
    return {"status": "reset"}
