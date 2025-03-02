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
        soup = self.get_soup(self.toc_url)
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
                [Chapter(self, a.text.strip(), a["href"]) for a in entries.select("a")],
            )
            for title, entries in zip(arc_titles, arc_entries, strict=True)
        ]
        return structure

    def parse_chapter(self, chapter: Chapter, content_raw: str | None = None) -> str:
        soup = self.get_soup(chapter.url, content_raw)
        body = soup.select_one("div.entry-content")
        cleaned = [f"<h2>{chapter.title}</h2>"]

        """
        0: nothing found
        1: first hr or image found
        2: second hr found, we can start copying
        """
        stage = 0

        for tag in body.children:
            if tag.name is None:
                continue

            if stage != 2:
                # ignore "previous epilogue/next epilogue" - wait until we see
                # the first image + one hr tag (main story) OR two hr tags (for epilogue)
                # include non-link headers (these are sometimes h1s or p with strongs)
                if tag.name == "hr":
                    stage += 1
                elif tag.name == "p" and tag.find("img"):
                    stage += 1
                elif (
                    tag.name == "h1" or tag.name == "p" and tag.find("strong") and not tag.find("a")
                ):
                    cleaned.append(f"<p><strong>{tag.text}</strong></p>")
                continue
            elif tag.name == "hr":
                # end of chapter
                break
            cleaned.append(str(tag))
        return "\n".join(cleaned)


def get_class() -> type[BaseSource]:
    return SourcePale
