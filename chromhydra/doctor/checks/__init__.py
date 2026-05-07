from chromhydra.doctor.checks.automation import headless_marker, webdriver_flag
from chromhydra.doctor.checks.client_hints import hints_platform, hints_present, sec_ch_header
from chromhydra.doctor.checks.consistency import (
    accept_language,
    header_user_agent,
    navigator_platform,
    worker_consistency,
)
from chromhydra.doctor.checks.hardware import webgl_renderer
from chromhydra.doctor.checks.network import ip_timezone

ALL_CHECKS = (
    webdriver_flag,
    headless_marker,
    hints_present,
    hints_platform,
    sec_ch_header,
    navigator_platform,
    header_user_agent,
    accept_language,
    worker_consistency,
    webgl_renderer,
    ip_timezone,
)
