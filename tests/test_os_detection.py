import pytest

from chromhydra.hints.os_family import os_family
from chromhydra.hints.os_from_navigator_platform import os_from_navigator_platform
from chromhydra.hints.os_from_user_agent import os_from_user_agent
from tests.agents import ANDROID, LINUX, MAC, WINDOWS


@pytest.mark.parametrize(
    "agent, expected",
    [(WINDOWS, "Windows"), (MAC, "macOS"), (LINUX, "Linux"), (ANDROID, "Android"), ("curl/8", "Unknown")],
)
def test_os_from_user_agent(agent, expected):
    assert os_from_user_agent(agent) == expected


@pytest.mark.parametrize(
    "platform, expected",
    [("Win32", "Windows"), ("MacIntel", "macOS"), ("Linux x86_64", "Linux"), ("iPhone", "iOS"), ("", "Unknown")],
)
def test_os_from_navigator_platform(platform, expected):
    assert os_from_navigator_platform(platform) == expected


def test_android_is_linux_family():
    assert os_family("Android") == os_family("Linux")
