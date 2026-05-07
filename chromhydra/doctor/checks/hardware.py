from chromhydra.doctor.finding import FAIL, PASS, WARN, Finding
from chromhydra.hints.os_family import os_family
from chromhydra.hints.os_from_user_agent import os_from_user_agent

SOFTWARE_RENDERERS = ("SwiftShader", "llvmpipe", "Software")
GPU_MARKERS = (("Apple", "macOS"), ("Metal", "macOS"), ("Direct3D", "Windows"), ("D3D11", "Windows"))


def webgl_renderer(fp: dict) -> Finding:
    title = "WebGL GPU"
    renderer = fp.get("renderer") or ""
    if not renderer:
        return Finding("webgl", title, WARN, "WebGL is unavailable")
    if any(marker in renderer for marker in SOFTWARE_RENDERERS):
        return Finding("webgl", title, WARN, f"software GPU ({renderer}), typical of servers and VMs")
    gpu_os = next((name for marker, name in GPU_MARKERS if marker in renderer), None)
    ua_os = os_from_user_agent(fp.get("ua", ""))
    if gpu_os and os_family(gpu_os) != os_family(ua_os):
        fix = "A JS-level tool can't hide the GPU; keep your real OS or use a patched binary"
        return Finding("webgl", title, FAIL, f"GPU looks like {gpu_os} but UA says {ua_os}", fix)
    return Finding("webgl", title, PASS, renderer)
