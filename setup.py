# =====================================
# generator=datazen
# version=3.1.3
# hash=a13929149030d15ffef9467595f314b4
# =====================================

"""
conntextual - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from conntextual_bootstrap.setup import setup  # type: ignore

# internal
from conntextual import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.11",
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
