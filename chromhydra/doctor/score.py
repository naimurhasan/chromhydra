from chromhydra.doctor.finding import PASS, SKIP, Finding


def score(findings: list[Finding]) -> tuple[int, int]:
    counted = [finding for finding in findings if finding.status != SKIP]
    return sum(finding.status == PASS for finding in counted), len(counted)
