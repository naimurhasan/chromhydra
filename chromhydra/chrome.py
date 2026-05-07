from seleniumbase import sb_cdp

from chromhydra.patch.install import install


class Chrome(sb_cdp.Chrome):
    def __init__(self, url=None, **kwargs):
        install()
        super().__init__(url, **kwargs)
