from chromhydra.doctor.finding import Finding
from chromhydra.doctor.score import score


def verdict(findings: list[Finding]) -> str:
    healthy, total = score(findings)
    if healthy == total:
        return f"🐉 all {total} heads healthy"
    return f"🩸 {healthy}/{total} heads healthy"
