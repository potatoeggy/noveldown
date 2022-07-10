from dataclasses import dataclass


@dataclass(frozen=True)
class Chapter:
    title: str
    """
    Chapter title
    """
    url: str
    cleaned_content: str | None
    """
    CLEANED HTML body
    """


class BaseSource:
    """
    Override this class!
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

    _chapter_urls: list[str] | None = None

    def __init__(self) -> None:
        pass

    @property
    def chapter_urls(self) -> list[str]:
        if self._chapter_urls is None:
            self._chapter_urls = self.fetch_chapter_list()
        return self._chapter_urls

    def update_metadata(self) -> None:
        """
        If needed, a function to dynamically set metadata vars.

        Override if necessary.
        """

    def fetch_chapter_list(self) -> list[str]:
        """
        Return a list of chapter URLs in ascending order.
        """
        raise NotImplementedError

    def parse_chapter(self, url: str) -> str:
        """
        Given a chapter URL, return clean HTML to be put
        directly into the EPUB.
        """
        raise NotImplementedError
