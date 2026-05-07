import json
from importlib.resources import files

PROBE = files("chromhydra.doctor").joinpath("probe.js").read_text()


def probe_script(echo_url: str | None, ip_url: str | None) -> str:
    return PROBE.replace("__ECHO_URL__", json.dumps(echo_url)).replace("__IP_URL__", json.dumps(ip_url))
