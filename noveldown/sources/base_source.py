from __future__ import annotations

import textwrap
from functools import cached_property
from typing import cast

import httpx
import requests
from bs4 import BeautifulSoup


class Chapter:
    def __init__(self, source: BaseSource, title: str, url: str) -> None:
        self._chapter_getter = source.parse_chapter
        self.title = title
        self.url = url
        self.content_raw: str | None = None

    def __repr__(self) -> str:
        return f"Chapter(title={self.title}, url={self.url})"

    @property
    def content(self) -> str:
        return self._chapter_getter(self, self.content_raw)

    async def get_raw_content(self, client: httpx.AsyncClient) -> str:
        """
        Fetch the raw page HTML and save it, returning the title.
        """
        # i love it when i spaghetti things for the sake of perf
        res = await client.get(self.url)
        self.content_raw = res.text

        if not res.text.strip():
            self.content_raw = requests.get(self.url).text
        return self.title


SectionedChapterList = list[tuple[str, list[Chapter]]]


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
     - `parse_chapter(chapter: Chapter, content_raw: str | None = None) -> str`
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

    # default section title for flattened or a or sentinel would be best
    # so that all chapter_urls are list[tuple]s
    _chapter_urls: list[Chapter] | SectionedChapterList | None = None

    def __init__(self) -> None:
        self.update_metadata()

        # assume populate
        if self.chapters:
            pass

    @property
    def chapters(self) -> list[Chapter] | SectionedChapterList:
        if self._chapter_urls is None:
            self._chapter_urls = self.fetch_chapter_list()
        return self._chapter_urls

    @cached_property
    def chapters_flattened(self) -> list[Chapter]:
        if self.chapters:
            if isinstance(self.chapters[0], tuple):

                flat_list: list[Chapter] = []
                for section in cast(SectionedChapterList, self.chapters):
                    _, chapters = section
                    for chap in chapters:
                        flat_list.append(chap)

                return flat_list

        # self.chapters is guaranteed to be a list, so
        # if the first check evaluates false it must be an empty list
        # which is the correct return type
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
        for section in cast(SectionedChapterList, self._chapter_urls) or []:
            sec_title, chapters = section
            for chap in chapters:
                if start <= current_num < end:
                    new_temp.append((sec_title, chap))
                current_num += 1

        new_chapter_urls: SectionedChapterList = []
        last_sec_title = "SENTINEL_IGNORE_EGG_NOVELDOWN"
        for sec_title, chap in new_temp:
            if last_sec_title != sec_title:
                new_chapter_urls.append((sec_title, []))
            last_sec_title = sec_title
            new_chapter_urls[-1][1].append(chap)
        self._chapter_urls = new_chapter_urls

    def get_soup(self, url: str, content_raw: str | None = None) -> BeautifulSoup:
        if content_raw is not None:
            if content_raw.strip():
                # if it is an empty page we go again
                return BeautifulSoup(content_raw, "lxml")
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

    def fetch_chapter_list(self) -> list[Chapter] | SectionedChapterList:
        """
        Return a list of chapter URLs in ascending order.

        Or, return a nested list of chapter URLs in ascending order (useful
        for webnovels with multiple volumes that should be separated).
        """
        raise NotImplementedError

    def parse_chapter(self, chapter: Chapter, content_raw: str | None = None) -> str:
        """
        Given a chapter URL, return clean HTML to be put
        directly into the EPUB.

        :param `content_raw`: parse an already-downloaded HTML file.
        """
        raise NotImplementedError
