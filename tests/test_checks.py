import pytest

from chromhydra.doctor.checks.automation import headless_marker, webdriver_flag
from chromhydra.doctor.checks.client_hints import hints_platform, hints_present, sec_ch_header
from chromhydra.doctor.checks.consistency import accept_language, header_user_agent, navigator_platform, worker_consistency
from chromhydra.doctor.checks.hardware import webgl_renderer
from chromhydra.doctor.checks.network import ip_timezone
from chromhydra.doctor.diagnose import diagnose
from chromhydra.doctor.finding import FAIL, PASS, SKIP, WARN
from tests.agents import WINDOWS


def statuses(fp):
    return {finding.id: finding.status for finding in diagnose(fp)}


def test_vanilla_headless_leaks_client_hints(load):
    result = statuses(load("vanilla_headless"))
    assert result["hints"] == FAIL
    assert result["sec-ch-ua"] == FAIL
    assert result["hints-os"] == SKIP


def test_hydra_headless_is_clean(load):
    assert set(statuses(load("hydra_headless")).values()) == {PASS}


def test_hydra_disguise_reports_what_cdp_cannot_fix(load):
    result = statuses(load("hydra_disguised"))
    assert result["hints"] == result["sec-ch-ua"] == result["hints-os"] == PASS
    assert result["worker"] == result["webgl"] == result["ip-tz"] == FAIL


def test_worker_detail_names_the_field(load):
    assert "platform" in worker_consistency(load("hydra_disguised")).detail


def test_webdriver_flag():
    assert webdriver_flag({"webdriver": True}).status == FAIL
    assert webdriver_flag({"webdriver": False}).status == PASS


@pytest.mark.parametrize(
    "fp",
    [
        {"ua": "HeadlessChrome/155"},
        {"ua": "", "brands": ["HeadlessChrome"]},
        {"ua": "", "headers": {"user-agent": "HeadlessChrome"}},
        {"ua": "", "worker": {"ua": "HeadlessChrome"}},
    ],
)
def test_headless_marker_everywhere(fp):
    assert headless_marker(fp).status == FAIL


def test_hints_platform_mismatch():
    assert hints_platform({"ua": WINDOWS, "brands": ["Chromium"], "uadPlatform": "macOS"}).status == FAIL


def test_hints_present_lists_brands():
    assert hints_present({"brands": ["A", "B"]}).detail == "A, B"


def test_sec_ch_header_platform_mismatch():
    fp = {"ua": WINDOWS, "headers": {"sec-ch-ua": "x", "sec-ch-ua-platform": '"macOS"'}}
    assert sec_ch_header(fp).status == FAIL


@pytest.mark.parametrize("check", [sec_ch_header, header_user_agent, accept_language])
def test_header_checks_skip_without_echo(check):
    assert check({"headers": None}).status == SKIP


def test_navigator_platform_mismatch():
    assert navigator_platform({"ua": WINDOWS, "platform": "MacIntel"}).status == FAIL


def test_header_user_agent_mismatch():
    assert header_user_agent({"ua": "a", "headers": {"user-agent": "b"}}).status == FAIL


def test_accept_language_mismatch_is_warning():
    assert accept_language({"lang": "en-US", "headers": {"accept-language": "bn-BD,bn;q=0.9"}}).status == WARN


def test_silent_worker_is_warning():
    assert worker_consistency({"worker": None}).status == WARN


@pytest.mark.parametrize(
    "renderer, status",
    [
        ("", WARN),
        ("ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)), SwiftShader driver)", WARN),
        ("ANGLE (Apple, ANGLE Metal Renderer: Apple M2, Unspecified Version)", FAIL),
        ("ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11)", PASS),
    ],
)
def test_webgl_against_windows_agent(renderer, status):
    assert webgl_renderer({"ua": WINDOWS, "renderer": renderer}).status == status


def test_ip_timezone_suggests_fix():
    finding = ip_timezone({"tz": "America/New_York", "ip": {"timezone": "Asia/Dhaka", "country": "BD"}})
    assert finding.status == FAIL
    assert 'timezone="Asia/Dhaka"' in finding.fix


def test_ip_timezone_skips_without_ip():
    assert ip_timezone({}).status == SKIP
