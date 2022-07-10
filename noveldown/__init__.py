from .api import (  # isort: skip
    download,
    download_progress,
    query,
)

__version__ = (0, 1, 0)
__version_str__ = ".".join(map(str, __version__))
