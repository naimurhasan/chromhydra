import pytest

from chromhydra.doctor.diagnose import diagnose
from chromhydra.doctor.finding import FAIL, PASS, SKIP
from chromhydra.doctor.fingerprint import fingerprint
from chromhydra.hints.host_info import host_info
from tests.agents import LINUX, WINDOWS

pytestmark = pytest.mark.browser
URL = "https://example.com"
ECHO = "https://httpbin.org/headers"


def statuses(hydra, **options):
    fp = fingerprint(hydra, URL, ECHO, None, headless=True, **options)
    return {finding.id: finding.status for finding in diagnose(fp)}


def test_vanilla_seleniumbase_has_empty_client_hints():
    assert statuses(False)["hints"] == FAIL


def test_chromhydra_restores_client_hints():
    result = statuses(True)
    assert result["hints"] == result["hints-os"] == result["headless"] == PASS
    assert result["sec-ch-ua"] in (PASS, SKIP)


def test_doctor_catches_worker_leak_when_spoofing_another_os():
    agent, platform = (LINUX, "Linux x86_64") if host_info()["os"] == "Windows" else (WINDOWS, "Win32")
    result = statuses(True, agent=agent, platform=platform)
    assert result["hints-os"] == PASS
    assert result["worker"] == FAIL
