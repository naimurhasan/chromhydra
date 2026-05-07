from chromhydra.doctor.finding import FAIL, PASS, SKIP, Finding
from chromhydra.hints.os_family import os_family
from chromhydra.hints.os_from_user_agent import os_from_user_agent

FIX = "chromhydra.install()"


def hints_present(fp: dict) -> Finding:
    title = "Client Hints"
    brands = fp.get("brands", [])
    if not brands:
        return Finding("hints", title, FAIL, "navigator.userAgentData.brands is empty, real Chrome reports 3", FIX)
    return Finding("hints", title, PASS, ", ".join(brands))


def hints_platform(fp: dict) -> Finding:
    title = "UA vs Client Hints OS"
    if not fp.get("brands"):
        return Finding("hints-os", title, SKIP, "no Client Hints to compare")
    ua_os = os_from_user_agent(fp.get("ua", ""))
    hint_os = fp.get("uadPlatform", "")
    if os_family(ua_os) != os_family(hint_os):
        return Finding("hints-os", title, FAIL, f"UA says {ua_os}, userAgentData says {hint_os or 'nothing'}", FIX)
    return Finding("hints-os", title, PASS, f"both say {ua_os}")


def sec_ch_header(fp: dict) -> Finding:
    title = "Sec-CH-UA header"
    headers = fp.get("headers")
    if headers is None:
        return Finding("sec-ch-ua", title, SKIP, "echo server unreachable")
    if not headers.get("sec-ch-ua"):
        return Finding("sec-ch-ua", title, FAIL, "HTTPS requests go out without Sec-CH-UA", FIX)
    ua_os = os_from_user_agent(fp.get("ua", ""))
    header_os = headers.get("sec-ch-ua-platform", "").strip('"')
    if os_family(ua_os) != os_family(header_os):
        return Finding("sec-ch-ua", title, FAIL, f"UA says {ua_os}, Sec-CH-UA-Platform says {header_os}", FIX)
    return Finding("sec-ch-ua", title, PASS, headers["sec-ch-ua"])
