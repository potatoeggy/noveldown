from pathlib import Path

from . import sources
from .sources.base_source import BaseSource, Chapter
from .utils import create_epub


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


def download_progress(
    novel: str | BaseSource,
    path: Path | str = ".",
    start: int | None = None,
    end: int | None = None,
) -> None:
    """
    Download a novel given an ID or source.

    Returns an iterable that iterates for each chapter downloaded.

    :param `start`: the zero-indexed first chapter to download.
    :param `end`: the zero-indexed chapter to stop at (exclusive)
    """
    path = Path(path)

    if isinstance(novel, str):
        novel = query(novel)

    # TODO: super hacky please remove mandown influences
    novel._chapter_urls = novel._chapter_urls[start:end]

    # populate chapters
    for chapter in novel.chapters:
        print(chapter)
        if isinstance(chapter, Chapter):
            if chapter.content:  # populate
                pass
            continue

        # if chapter is a tuple[str, list[Chapter]]
        _, sublist = chapter
        for actual_chap in sublist:
            if actual_chap.content:
                pass

    create_epub(novel, path)


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
    # for _ in download_progress(novel, path):
    #    pass
    return download_progress(novel, path, start, end)
