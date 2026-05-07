from chromhydra.doctor.finding import Finding
from chromhydra.doctor.render.icons import ICONS
from chromhydra.doctor.render.verdict import verdict

WIDTH = 26


def report_text(findings: list[Finding], label: str) -> str:
    lines = [f"🐉 Chromhydra Doctor · {label}", "─" * 60]
    for finding in findings:
        lines.append(f"{ICONS[finding.status]} {finding.title:<{WIDTH}} {finding.detail}")
        if finding.fix:
            lines.append(f"   {'':<{WIDTH}} ↳ fix: {finding.fix}")
    return "\n".join([*lines, "", verdict(findings)])
