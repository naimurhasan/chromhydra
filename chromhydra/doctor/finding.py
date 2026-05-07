from dataclasses import dataclass

PASS = "pass"
WARN = "warn"
FAIL = "fail"
SKIP = "skip"


@dataclass(frozen=True)
class Finding:
    id: str
    title: str
    status: str
    detail: str = ""
    fix: str = ""
