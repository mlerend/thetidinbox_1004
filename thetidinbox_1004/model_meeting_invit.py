def classify_meeting_invit(email_text):
    keywords = ["invitation","meeting", "date", "time", "agenda", "attendees", "RSVP", "confirm", "required", "optional", "accept","decline", "join", "call", "zoom", "teams", "schedule", "appointment", "conference", "webinar", "Microsoft Teams", "Zoom meeting", "Google Calendar", "Meeting ID","join the meeting","zoom.us", "Click here", "Meeting Room","join","download"]
    email_text = email_text.lower()

    count = 0
    for keyword in keywords:
        if keyword in email_text:
            count += 1

    if count >= 5:
        return 1

    return 0
