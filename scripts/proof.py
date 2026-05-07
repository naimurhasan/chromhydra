import sys
from pathlib import Path

from seleniumbase import sb_cdp

from chromhydra.patch.install import install, uninstall

SITES = {
    "httpbin-headers": ("https://httpbin.org/headers", 2),
    "browserleaks-client-hints": ("https://browserleaks.com/client-hints", 6),
    "sannysoft": ("https://bot.sannysoft.com", 6),
    "deviceandbrowserinfo": ("https://deviceandbrowserinfo.com/are_you_a_bot", 8),
    "browserscan": ("https://www.browserscan.net/bot-detection", 12),
}
MODES = {"seleniumbase": uninstall, "chromhydra": install}


def capture(folder: Path, mode: str) -> None:
    sb = sb_cdp.Chrome(headless=True)
    try:
        for name, (url, wait) in SITES.items():
            try:
                sb.open(url)
                sb.sleep(wait)
                sb.save_screenshot(f"{name}-{mode}.png", str(folder))
                print(f"📸 {name}-{mode}.png")
            except Exception as error:
                print(f"⚠️ {name}-{mode}: {error}")
    finally:
        sb.driver.stop()


def main(out_dir: str) -> None:
    folder = Path(out_dir)
    folder.mkdir(parents=True, exist_ok=True)
    for mode, prepare in MODES.items():
        prepare()
        capture(folder, mode)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs/proof")
