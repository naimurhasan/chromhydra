import json

from chromhydra.doctor.chrome_options import chrome_options
from chromhydra.doctor.diagnose import diagnose
from chromhydra.doctor.finding import FAIL
from chromhydra.doctor.fingerprint import fingerprint
from chromhydra.doctor.render.compare_text import compare_text
from chromhydra.doctor.render.markdown import markdown
from chromhydra.doctor.render.report_text import report_text

IP_URL = "https://ipinfo.io/json"
MODES = {"vanilla": {"SeleniumBase": False}, "hydra": {"Chromhydra": True}}
MODES["compare"] = {**MODES["vanilla"], **MODES["hydra"]}


def run_doctor(args) -> int:
    options = chrome_options(
        args.headed,
        agent=args.agent,
        platform=args.platform,
        timezone=args.timezone,
        locale=args.locale,
        proxy=args.proxy,
    )
    ip_url = IP_URL if args.ip else None
    prints = {label: fingerprint(hydra, args.url, args.echo_url, ip_url, **options) for label, hydra in MODES[args.mode].items()}
    results = {label: diagnose(fp) for label, fp in prints.items()}
    label, findings = next(iter(results.items()))
    print(compare_text(results) if len(results) > 1 else report_text(findings, label))
    if args.json_path:
        with open(args.json_path, "w") as handle:
            json.dump(prints, handle, indent=2)
    if args.markdown_path:
        with open(args.markdown_path, "a") as handle:
            handle.write(markdown(results, args.title))
    return int(args.strict and any(finding.status == FAIL for finding in list(results.values())[-1]))
