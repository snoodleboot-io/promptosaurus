"""promptosaurus — prompt library build tool."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("promptosaurus")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["__version__"]
