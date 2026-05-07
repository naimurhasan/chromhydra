from chromhydra.doctor.finding import FAIL, PASS, SKIP, Finding


def ip_timezone(fp: dict) -> Finding:
    title = "IP vs timezone"
    ip = fp.get("ip") or {}
    if not ip.get("timezone"):
        return Finding("ip-tz", title, SKIP, "run with --ip to check")
    if ip["timezone"] != fp.get("tz"):
        detail = f"exit IP is in {ip['timezone']} ({ip.get('country')}), browser says {fp.get('tz')}"
        return Finding("ip-tz", title, FAIL, detail, f"Pass timezone=\"{ip['timezone']}\"")
    return Finding("ip-tz", title, PASS, ip["timezone"])
