from pathlib import Path
from typing import Iterator

from . import sources
from .sources.base_source import BaseSource
from .utils import create_epub, load_all_chapters


def get_available_ids() -> list[str]:
    """
    Return a list of recognised webnovel IDs.
    """
    return [s.id for s in sources.get_all_classes()]


def query(novel_id: str) -> BaseSource:
    """
    Attempt to query for a webnovel given an ID.
    :param `novel_id`: An ID to search for
    :raises `ValueError` if no sources found.
    """
    return sources.get_class_for(novel_id)()


def prefetch_book(novel: BaseSource) -> Iterator[str]:
    """
    Really quickly download chapters into memory.
    Call `download` or `download_progress` afterward
    to convert it.
    """
    yield from load_all_chapters(novel)


def download_progress(
    novel: str | BaseSource,
    path: Path | str = ".",
    start: int | None = None,
    end: int | None = None,
) -> Iterator[str]:
    """
    Download a novel given an ID or source.

    Returns an iterable that iterates for each chapter downloaded.

    :param `start`: the zero-indexed first chapter to download.
    :param `end`: the zero-indexed chapter to stop at (exclusive)
    """
    path = Path(path)

    if isinstance(novel, str):
        novel = query(novel)

    novel.set_chapter_range(start=start, end=end)

    yield from create_epub(novel, path)


def download(
    novel: str | BaseSource,
    path: Path | str = ".",
    start: int | None = None,
    end: int | None = None,
) -> None:
    """
    Download a novel given an ID or source.

    :param `start`: the zero-indexed first chapter to download.
    :param `end`: the zero-indexed chapter to stop at (exclusive)
    """
    for _ in download_progress(novel, path, start, end):
        pass
