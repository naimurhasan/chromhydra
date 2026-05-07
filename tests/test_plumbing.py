import json

from chromhydra.cli import parser
from chromhydra.doctor.chrome_options import chrome_options
from chromhydra.doctor.probe_script import probe_script
from chromhydra.patch.install import install, installed, uninstall


def test_chrome_options_drop_empty_values():
    assert chrome_options(False, agent=None, timezone="Asia/Dhaka") == {"headless": True, "timezone": "Asia/Dhaka"}


def test_probe_script_injects_urls():
    script = probe_script("https://echo.test/headers", None)
    assert json.dumps("https://echo.test/headers") in script
    assert "const ipUrl = null;" in script
    assert "__" not in script.split("const ipUrl")[0].split("const echoUrl")[1]


def test_cli_defaults():
    args = parser().parse_args(["doctor"])
    assert (args.mode, args.headed, args.ip, args.strict) == ("hydra", False, False, False)


def test_install_round_trip():
    install()
    assert installed()
    uninstall()
    assert not installed()
