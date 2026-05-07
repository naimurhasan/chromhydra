PREFIXES = (("Win", "Windows"), ("Mac", "macOS"), ("Linux", "Linux"), ("iP", "iOS"))


def os_from_navigator_platform(platform: str) -> str:
    return next((name for prefix, name in PREFIXES if platform.startswith(prefix)), "Unknown")
