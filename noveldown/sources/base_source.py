from dataclasses import InitVar, dataclass, field
from typing import Callable

import requests
from bs4 import BeautifulSoup


@dataclass
class Chapter:
    source: InitVar["BaseSource"]
    title: str
    url: str

    _chapter_getter: Callable[[str], str] = field(init=False)

    def __post_init__(self, source: "BaseSource") -> None:
        self._chapter_getter = source.parse_chapter

    @property
    def content(self) -> str:
        return self._chapter_getter(self.url)


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
     - `parse_chapter(url: str) -> str`
    """

    # begin metadata vars (override them)
    id: str = "0"
    title: str = ""
    authors: list[str] = []
    url: str = ""
    genres: list[str] = []
    description: str = ""
    cover_url: str = ""
    # end metadata vars

    _chapter_urls: list[Chapter] | list[tuple[str, list[Chapter]]] | None = None

    def __init__(self) -> None:
        self.update_metadata()

    @property
    def chapters(self) -> list[Chapter] | list[tuple[str, list[Chapter]]]:
        if self._chapter_urls is None:
            self._chapter_urls = self.fetch_chapter_list()
        return self._chapter_urls

    def get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url).text, "lxml")

    def get_text_from_url(self, url: str) -> str:
        return requests.get(url).text

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

    def parse_chapter(self, url: str) -> str:
        """
        Given a chapter URL, return clean HTML to be put
        directly into the EPUB.
        """
        raise NotImplementedError
