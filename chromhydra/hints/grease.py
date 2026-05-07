GREASE_CHARS = (" ", "(", ":", "-", ".", "/", ")", ";", "=", "?", "_")
GREASE_VERSIONS = ("8", "99", "24")


def greased_brand(major: int) -> tuple[str, str]:
    left = GREASE_CHARS[major % len(GREASE_CHARS)]
    right = GREASE_CHARS[(major + 1) % len(GREASE_CHARS)]
    return f"Not{left}A{right}Brand", GREASE_VERSIONS[major % len(GREASE_VERSIONS)]
