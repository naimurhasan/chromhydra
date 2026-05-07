MARKERS = (
    ("Android", "Android"),
    ("Windows", "Windows"),
    ("Macintosh", "macOS"),
    ("CrOS", "Chrome OS"),
    ("Linux", "Linux"),
    ("X11", "Linux"),
)


def os_from_user_agent(user_agent: str) -> str:
    return next((name for marker, name in MARKERS if marker in user_agent), "Unknown")
