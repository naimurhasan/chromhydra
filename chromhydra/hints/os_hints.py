DEFAULTS = {
    "Windows": {"platform_version": "19.0.0", "architecture": "x86"},
    "macOS": {"platform_version": "15.5.0", "architecture": "arm"},
    "Linux": {"platform_version": "6.8.0", "architecture": "x86"},
}
UNKNOWN = {"platform_version": "", "architecture": ""}


def os_hints(os_name: str, host: dict) -> dict:
    if host["os"] == os_name:
        return {
            "platform": os_name,
            "platform_version": host["platform_version"],
            "architecture": host["architecture"],
        }
    return {"platform": os_name, **DEFAULTS.get(os_name, UNKNOWN)}
