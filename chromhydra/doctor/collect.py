import json

from chromhydra.doctor.probe_script import probe_script


def collect(sb, echo_url: str | None, ip_url: str | None) -> dict:
    script = probe_script(echo_url, ip_url)
    return json.loads(sb.loop.run_until_complete(sb.page.evaluate(script, await_promise=True)))
