from chromhydra.chrome import Chrome
from chromhydra.doctor.diagnose import diagnose
from chromhydra.hints.client_hints import client_hints
from chromhydra.patch.install import install, installed, uninstall

__version__ = "0.1.0"
__all__ = ["Chrome", "client_hints", "diagnose", "install", "installed", "uninstall"]
