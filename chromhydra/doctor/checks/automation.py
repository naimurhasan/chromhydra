from chromhydra.doctor.finding import FAIL, PASS, Finding


def webdriver_flag(fp: dict) -> Finding:
    title = "navigator.webdriver"
    if fp.get("webdriver"):
        return Finding("webdriver", title, FAIL, "navigator.webdriver is true", "Use CDP Mode instead of plain WebDriver")
    return Finding("webdriver", title, PASS, "hidden")


def headless_marker(fp: dict) -> Finding:
    title = "Headless marker"
    worker = fp.get("worker") or {}
    headers = fp.get("headers") or {}
    sources = [fp.get("ua", ""), headers.get("user-agent", ""), worker.get("ua", ""), *fp.get("brands", [])]
    if any("Headless" in source for source in sources):
        return Finding("headless", title, FAIL, "'Headless' shows up in the UA or brands", "chromhydra.install()")
    return Finding("headless", title, PASS, "no 'Headless' anywhere")
