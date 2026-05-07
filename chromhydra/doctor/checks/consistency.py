from chromhydra.doctor.finding import FAIL, PASS, SKIP, WARN, Finding
from chromhydra.hints.os_family import os_family
from chromhydra.hints.os_from_navigator_platform import os_from_navigator_platform
from chromhydra.hints.os_from_user_agent import os_from_user_agent

WORKER_FIELDS = ("ua", "platform", "lang", "tz", "brands")


def navigator_platform(fp: dict) -> Finding:
    title = "UA vs navigator.platform"
    ua_os = os_from_user_agent(fp.get("ua", ""))
    platform_os = os_from_navigator_platform(fp.get("platform", ""))
    if os_family(ua_os) != os_family(platform_os):
        detail = f"UA says {ua_os}, navigator.platform is {fp.get('platform')!r}"
        return Finding("nav-platform", title, FAIL, detail, "Pass platform= matching your UA")
    return Finding("nav-platform", title, PASS, fp.get("platform", ""))


def header_user_agent(fp: dict) -> Finding:
    title = "Header UA vs JS UA"
    headers = fp.get("headers")
    if headers is None:
        return Finding("header-ua", title, SKIP, "echo server unreachable")
    if headers.get("user-agent") != fp.get("ua"):
        return Finding("header-ua", title, FAIL, "the User-Agent header differs from navigator.userAgent")
    return Finding("header-ua", title, PASS, "identical")


def accept_language(fp: dict) -> Finding:
    title = "Accept-Language"
    headers = fp.get("headers")
    if headers is None:
        return Finding("language", title, SKIP, "echo server unreachable")
    header_lang = headers.get("accept-language", "").split(",")[0].split(";")[0]
    if header_lang != fp.get("lang"):
        detail = f"header says {header_lang!r}, navigator.language is {fp.get('lang')!r}"
        return Finding("language", title, WARN, detail, "Pass locale= once, not separately")
    return Finding("language", title, PASS, header_lang)


def worker_consistency(fp: dict) -> Finding:
    title = "Web Worker"
    worker = fp.get("worker")
    if not worker:
        return Finding("worker", title, WARN, "the worker never answered")
    diffs = [f"{field} ({worker.get(field)!r} vs {fp.get(field)!r})" for field in WORKER_FIELDS if worker.get(field) != fp.get(field)]
    if diffs:
        fix = "CDP can't override worker navigator.platform; keep your real OS or use a patched binary"
        return Finding("worker", title, FAIL, "worker disagrees on " + "; ".join(diffs), fix)
    return Finding("worker", title, PASS, "worker matches the page")
