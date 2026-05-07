from chromhydra.hints.brand_list import brand_list
from chromhydra.hints.os_from_user_agent import os_from_user_agent
from chromhydra.hints.os_hints import os_hints


def client_hints(user_agent: str, full_version: str, host: dict) -> dict:
    brands = brand_list(full_version)
    return {
        **os_hints(os_from_user_agent(user_agent), host),
        "model": "",
        "mobile": "Mobile" in user_agent,
        "brands": [{"brand": b["brand"], "version": b["version"]} for b in brands],
        "full_version_list": [{"brand": b["brand"], "version": b["full_version"]} for b in brands],
        "full_version": full_version,
        "bitness": "64",
        "wow64": False,
    }
