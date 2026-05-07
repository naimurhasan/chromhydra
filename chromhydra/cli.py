import argparse

from chromhydra.doctor.command import MODES, run_doctor


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="chromhydra", description="Cut the leaks before they grow back.")
    commands = root.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor", help="audit the browser fingerprint for leaks")
    doctor.add_argument("--mode", choices=list(MODES), default="hydra", help="hydra, vanilla SeleniumBase, or compare both")
    doctor.add_argument("--headed", action="store_true", help="show the browser window")
    doctor.add_argument("--agent", help="user agent to present")
    doctor.add_argument("--platform", help="navigator.platform to present, e.g. Win32")
    doctor.add_argument("--timezone", help="IANA timezone, e.g. America/New_York")
    doctor.add_argument("--locale", help="locale, e.g. en-US")
    doctor.add_argument("--proxy", help="proxy as host:port or user:pass@host:port")
    doctor.add_argument("--url", default="https://example.com", help="page to run the probe on")
    doctor.add_argument("--echo-url", default="https://httpbin.org/headers", help="header echo endpoint")
    doctor.add_argument("--ip", action="store_true", help="compare the exit IP timezone via ipinfo.io")
    doctor.add_argument("--json", dest="json_path", help="save raw fingerprints as JSON")
    doctor.add_argument("--markdown", dest="markdown_path", help="append a Markdown report to this file")
    doctor.add_argument("--title", default="🐉 Chromhydra Doctor", help="Markdown report heading")
    doctor.add_argument("--strict", action="store_true", help="exit 1 when the last run has a failure")
    return root


def main(argv=None) -> int:
    return run_doctor(parser().parse_args(argv))
