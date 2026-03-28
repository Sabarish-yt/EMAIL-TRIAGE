from app.models import Email

EMAIL_DATA = {
    "easy": [
        Email(id="1", subject="Refund request", body="I want my money back", sender="user1"),
        Email(id="2", subject="Login issue", body="Cannot login to my account", sender="user2"),
    ],
    "medium": [
        Email(id="3", subject="Fraud alert", body="Unauthorized transaction detected", sender="user3"),
        Email(id="4", subject="Feature request", body="Please add dark mode", sender="user4"),
    ],
    "hard": [
        Email(id="5", subject="Angry complaint", body="Your service is terrible!!! Fix NOW", sender="user5"),
        Email(id="6", subject="Legal threat", body="I will sue your company", sender="user6"),
    ]
}
