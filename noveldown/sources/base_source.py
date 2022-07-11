import textwrap
from functools import cached_property

import requests
from bs4 import BeautifulSoup


class Chapter:
    def __init__(self, source: "BaseSource", title: str, url: str) -> None:
        self._chapter_getter = source.parse_chapter
        self.title = title
        self.url = url

    def __repr__(self) -> str:
        return f"Chapter(title={self.title}, url={self.url})"

    @property
    def content(self) -> str:
        return self._chapter_getter(self)


class BaseSource:
    """
    Override this class!

    Properties

     - `id: str`
     - `title: str`
     - `authors: list[str]`
     - `url: str`
     - `genres: list[str]`
     - `description: str`
     - `cover_url: str`

    Functions

     - `update_metadata -> None`
     - `fetch_chapter_list -> list[Chapter]`
     - `parse_chapter(chapter: Chapter) -> str`
    """

    # begin metadata vars (override them)
    id: str = "0"
    aliases: list[str] = []
    title: str = ""
    authors: list[str] = []
    url: str = ""
    genres: list[str] = []
    description: str = ""
    cover_url: str | None = None
    # end metadata vars

    _chapter_urls: list[Chapter] | list[tuple[str, list[Chapter]]] | None = None

    def __init__(self) -> None:
        self.update_metadata()

        # assume populate
        if self.chapters:
            pass

    @property
    def chapters(self) -> list[Chapter] | list[tuple[str, list[Chapter]]]:
        if self._chapter_urls is None:
            self._chapter_urls = self.fetch_chapter_list()
        return self._chapter_urls

    @cached_property
    def chapters_flattened(self) -> list[Chapter]:
        if self.chapters:
            if isinstance(self.chapters[0], tuple):
                flat_list: list[Chapter] = []
                for section in self.chapters:
                    assert isinstance(section, tuple)
                    _, chapters = section
                    for chap in chapters:
                        flat_list.append(chap)

                return flat_list
        # TODO: really fix by at least having a default section title or something
        return self.chapters  # type: ignore

    def set_chapter_range(
        self, *, start: int | None = None, end: int | None = None
    ) -> None:
        start = start or 0
        end = end or len(self.chapters_flattened)
        if self._chapter_urls and isinstance(self._chapter_urls[0], Chapter):
            self._chapter_urls = self._chapter_urls[start:end]
            return

        current_num = 0
        new_temp = []
        for section in self._chapter_urls:
            assert isinstance(section, tuple)
            sec_title, chapters = section
            for chap in chapters:
                if start <= current_num < end:
                    new_temp.append((sec_title, chap))
                current_num += 1

        new_chapter_urls: list[tuple[str, list[Chapter]]] = []
        last_sec_title = "SENTINEL_IGNORE_EGG_NOVELDOWN"
        for sec_title, chap in new_temp:
            if last_sec_title != sec_title:
                new_chapter_urls.append((sec_title, []))
            last_sec_title = sec_title
            new_chapter_urls[-1][1].append(chap)
        self._chapter_urls = new_chapter_urls

    def get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url).text, "lxml")

    def get_text_from_url(self, url: str) -> str:
        return requests.get(url).text

    def __repr__(self) -> str:
        return (
            textwrap.dedent(
                f"""
            {self.id}: {self.title} - {" ".join(self.authors)}
            url: {self.url}
            genres: {", ".join(self.genres)}
            cover: {self.cover_url}
            chapters: {len(self.chapters_flattened)}

            """
            )
            + self.description
        ).strip()

    def update_metadata(self) -> None:
        """
        If needed, a function to dynamically set metadata vars.

        Override if necessary.
        """

    def fetch_chapter_list(self) -> list[Chapter] | list[tuple[str, list[Chapter]]]:
        """
        Return a list of chapter URLs in ascending order.

        Or, return a nested list of chapter URLs in ascending order (useful
        for webnovels with multiple volumes that should be separated).
        """
        raise NotImplementedError

    def parse_chapter(self, chapter: Chapter) -> str:
        """
        Given a chapter URL, return clean HTML to be put
        directly into the EPUB.
        """
        raise NotImplementedError
