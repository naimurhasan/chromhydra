from chromhydra.doctor.checks import ALL_CHECKS
from chromhydra.doctor.finding import Finding


def diagnose(fp: dict, checks=ALL_CHECKS) -> list[Finding]:
    return [check(fp) for check in checks]
