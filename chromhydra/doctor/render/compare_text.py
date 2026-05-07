from chromhydra.doctor.finding import Finding
from chromhydra.doctor.render.icons import ICONS
from chromhydra.doctor.render.verdict import verdict

WIDTH = 26


def compare_text(results: dict[str, list[Finding]]) -> str:
    labels = list(results)
    header = f"   {'Check':<{WIDTH}} " + "  ".join(f"{label:^14}" for label in labels)
    lines = ["🐉 Chromhydra Doctor · " + " vs ".join(labels), header, "─" * len(header)]
    for row in zip(*results.values()):
        cells = "  ".join(f"{ICONS[finding.status]:^13}" for finding in row)
        lines.append(f"   {row[0].title:<{WIDTH}} {cells}")
    lines.append("")
    lines.extend(f"{label:>14}: {verdict(findings)}" for label, findings in results.items())
    return "\n".join(lines)
