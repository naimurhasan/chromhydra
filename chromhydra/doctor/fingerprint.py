from seleniumbase import sb_cdp

from chromhydra.doctor.collect import collect
from chromhydra.patch.install import install, uninstall


def fingerprint(hydra: bool, url: str, echo_url: str | None, ip_url: str | None, **options) -> dict:
    (install if hydra else uninstall)()
    sb = sb_cdp.Chrome(url, **options)
    try:
        return collect(sb, echo_url, ip_url)
    finally:
        sb.driver.stop()
