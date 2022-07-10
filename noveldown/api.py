from typing import Iterable

from . import sources
from .sources.base_source import BaseSource


def query(novel_id: str) -> BaseSource:
    """
    Attempt to query for a comic given an ID.
    :param `novel_id`: An ID to search for
    """
    return sources.get_class_for(novel_id)()


def download_progress(novel: str | BaseSource) -> Iterable[None]:
    """
    Download a novel given an ID or source.

    Returns an iterable that iterates for each chapter downloaded.
    """


def download(novel: str | BaseSource) -> None:
    """
    Download a novel given an ID or source.
    """
    for _ in download_progress(novel):
        pass
