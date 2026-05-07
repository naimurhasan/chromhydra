from chromhydra.doctor.finding import PASS, Finding
from chromhydra.doctor.render.icons import ICONS
from chromhydra.doctor.render.verdict import verdict


def markdown(results: dict[str, list[Finding]], heading: str = "🐉 Chromhydra Doctor") -> str:
    labels = list(results)
    lines = [
        f"## {heading}",
        "",
        "| Check | " + " | ".join(labels) + " |",
        "|---|" + "---|" * len(labels),
    ]
    for row in zip(*results.values()):
        lines.append(f"| {row[0].title} | " + " | ".join(ICONS[finding.status] for finding in row) + " |")
    lines.append("| **Verdict** | " + " | ".join(verdict(findings) for findings in results.values()) + " |")
    for label, findings in results.items():
        problems = [finding for finding in findings if finding.status != PASS]
        if problems:
            lines.extend(["", f"**{label}**", ""])
            lines.extend(f"- {ICONS[f.status]} **{f.title}**: {f.detail}" + (f" → _{f.fix}_" if f.fix else "") for f in problems)
    return "\n".join(lines) + "\n"
