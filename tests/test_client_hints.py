import pytest

from chromhydra.hints.client_hints import client_hints
from chromhydra.hints.os_hints import os_hints
from chromhydra.hints.padded_version import padded_version
from tests.agents import ANDROID, MAC, WINDOWS

MAC_HOST = {"os": "macOS", "platform_version": "15.3.1", "architecture": "arm"}


@pytest.mark.parametrize("raw, expected", [("15.3.1", "15.3.1"), ("15.3", "15.3.0"), ("6.8", "6.8.0"), ("1.2.3.4", "1.2.3")])
def test_padded_version(raw, expected):
    assert padded_version(raw) == expected


def test_host_os_uses_real_host_values():
    assert os_hints("macOS", MAC_HOST) == {"platform": "macOS", "platform_version": "15.3.1", "architecture": "arm"}


def test_foreign_os_uses_defaults():
    assert os_hints("Windows", MAC_HOST) == {"platform": "Windows", "platform_version": "19.0.0", "architecture": "x86"}


def test_mac_hints_match_captured_headed_chrome():
    hints = client_hints(MAC, "155.0.8059.85", MAC_HOST)
    assert hints["platform"] == "macOS"
    assert hints["platform_version"] == "15.3.1"
    assert hints["architecture"] == "arm"
    assert [b["brand"] for b in hints["brands"]] == ["Google Chrome", "Chromium", "Not(A:Brand"]
    assert hints["full_version_list"][2] == {"brand": "Not(A:Brand", "version": "24.0.0.0"}
    assert hints["mobile"] is False


def test_windows_disguise():
    assert client_hints(WINDOWS, "155.0.8059.85", MAC_HOST)["platform"] == "Windows"


def test_mobile_flag():
    assert client_hints(ANDROID, "155.0.8059.85", MAC_HOST)["mobile"] is True
