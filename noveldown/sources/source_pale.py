from .base_source import BaseSource, Chapter, SectionedChapterList

DESCRIPTION = """
There are three methods of becoming a practitioner: being part of a family of practitioners, stumbling across knowledge belonging to Others by chance, and finally, making direct deals with Others in order to gain their knowledge. The third happens to be the oldest, and the road our protagonists end up going down. Three teenagers, Verona, Lucy, and Avery, are awakened as practitioners in order to solve a mystery in the town of Kennet, Ontario.
""".strip()
TOC_URL = "https://palewebserial.wordpress.com/table-of-contents/"


class SourcePale(BaseSource):
    id = "Pale"
    aliases = ["PaleSerial"]
    title = "Pale"
    authors = ["Wildbow"]
    url = "https://palewebserial.wordpress.com"
    genres = [
        "Adventure",
        "Fantasy",
        "Magic",
        "Young Adult",
    ]
    description = DESCRIPTION
    toc_url = TOC_URL

    def fetch_chapter_list(self) -> SectionedChapterList:
        soup = self.get_soup(TOC_URL)
        toc_html = soup.select_one("div.entry-content")

        arc_titles = toc_html.select("div.entry-content > p:not([style]) > strong")
        arc_entries = toc_html.select("div.entry-content > p[style]")

        # a.text only gets the chapter semver because this site
        # is inconsistently formatted and leaves the POV in
        # `strong` tags sometimes and sometimes just leaves it
        # hanging
        structure = [
            (
                title.text,
                [Chapter(self, a.text, a["href"]) for a in entries.select("a")],
            )
            for title, entries in zip(arc_titles, arc_entries, strict=True)
        ]
        return structure

    def parse_chapter(self, chapter: Chapter, content_raw: str | None = None) -> str:
        soup = self.get_soup(chapter.url, content_raw)
        body = soup.select_one("div.entry-content")
        cleaned = [f"<h2>{chapter.title}</h2>"]

        is_chapter_begun = False
        for tag in body.children:
            if not is_chapter_begun:
                if tag.name == "hr":
                    is_chapter_begun = True
                continue
            elif tag.name == "hr":
                # end of chapter
                break
            cleaned.append(str(tag))

        return "\n".join(cleaned)


def get_class() -> type[BaseSource]:
    return SourcePale
