"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Lords International School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@lords.edu", "daniel@lords.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@lords.edu", "sophia@lords.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@lords.edu", "olivia@lords.edu"]
    }
,
    "Basketball Club": {
        "description": "Develop basketball skills and compete in friendly matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@lords.edu"]
    },
    "Tennis Club": {
        "description": "Master tennis techniques and participate in tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 10,
        "participants": ["sarah@lords.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and various art mediums",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["alice@lords.edu", "lucas@lords.edu"]
    },
    "Drama Club": {
        "description": "Perform in plays and develop acting and stage skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["grace@lords.edu"]
    },
    "Debate Club": {
        "description": "Engage in competitive debate and public speaking",
        "schedule": "Mondays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": ["nathan@lords.edu", "isabella@lords.edu"]
    },
    "Math Olympiad": {
        "description": "Prepare for mathematics competitions and problem-solving challenges",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["tyler@lords.edu"]
    }
}

# Validate student is not already signed up
def validate_signup(activity, email):
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400, detail="Student already signed up for this activity")
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(
            status_code=400, detail="Activity is full")
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate signup (duplicates + capacity)
    validate_signup(activity, email)

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a participant from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}