# =====================================
# generator=datazen
# version=3.1.3
# hash=c600a3dcba6fae2b59d2a9abb7decb36
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
        "3.8",
        "3.9",
        "3.10",
        "3.11",
    ],
}
setup(
    pkg_info,
    author_info,
)
