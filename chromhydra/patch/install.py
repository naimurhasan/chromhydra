from seleniumbase.undetected.cdp_driver.connection import Connection

from chromhydra.patch.set_user_agent import set_user_agent

ORIGINAL = Connection.__dict__["set_user_agent"]


def install() -> None:
    type.__setattr__(Connection, "set_user_agent", set_user_agent)


def uninstall() -> None:
    type.__setattr__(Connection, "set_user_agent", ORIGINAL)


def installed() -> bool:
    return Connection.__dict__["set_user_agent"] is set_user_agent
