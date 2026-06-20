from urllib.parse import quote

from src import app as app_module


def test_get_activities(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_activity_name in activities
    assert activities[expected_activity_name]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(activities[expected_activity_name]["participants"], list)


def test_signup_for_activity(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Signed up" in body["message"]
    assert email in app_module.activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected(client):
    # Arrange
    existing_email = "michael@mergington.edu"
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already registered for this activity"


def test_remove_participant(client):
    # Arrange
    email = "nina@mergington.edu"
    activity_name = "Soccer Team"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Removed" in body["message"]
    assert email not in app_module.activities[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    email = "missing@mergington.edu"
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_from_unknown_activity_returns_404(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity_name = "Nonexistent Club"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
