from .api import (  # isort: skip
    get_available_ids,
    download,
    download_progress,
    query,
)

__version__ = (1, 2, 2)
__version_str__ = ".".join(map(str, __version__))
