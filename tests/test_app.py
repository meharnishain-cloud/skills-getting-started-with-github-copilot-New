"""
Pytest tests for the FastAPI activities application.

Tests follow the AAA (Arrange-Act-Assert) pattern and reset in-memory state
between tests.
"""

import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure src is importable from the test run location.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities  # noqa: E402


# Keep a deep copy of the initial activities state so tests can reset it.
_INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activity state before/after each test."""
    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    """Return a FastAPI TestClient instance."""
    return TestClient(app)


def test_get_activities_includes_chess_club(client):
    # Arrange: (state already reset by fixture)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_adds_participant_and_returns_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@lords.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@lords.edu"  # Already signed up

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_delete_removes_participant_and_returns_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@lords.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_delete_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@lords.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()
