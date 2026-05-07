import platform

from chromhydra.hints.os_hints import DEFAULTS
from chromhydra.hints.padded_version import padded_version

SYSTEMS = {"Darwin": "macOS", "Windows": "Windows", "Linux": "Linux"}


def host_info() -> dict:
    os_name = SYSTEMS.get(platform.system(), platform.system())
    releases = {
        "macOS": platform.mac_ver()[0],
        "Linux": platform.release().split("-")[0],
    }
    release = releases.get(os_name) or DEFAULTS.get(os_name, {}).get("platform_version", "")
    machine = platform.machine().lower()
    return {
        "os": os_name,
        "platform_version": padded_version(release) if release else "",
        "architecture": "arm" if machine.startswith(("arm", "aarch")) else "x86",
    }
