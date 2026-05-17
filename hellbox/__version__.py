from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("hellbox")
except PackageNotFoundError:
    __version__ = "unknown"
