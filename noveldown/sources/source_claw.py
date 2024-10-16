from .base_source import BaseSource, Chapter, SectionedChapterList

DESCRIPTION = """
Joshua Munce, Sheila Hardy, Dan Whitely, Max Highland, Tonya Keifer, Marvin Su… this pair has many names, but those names aren’t their own; they’re names to sell.  In a rigged and crumbling system, the only way to get ahead is to circumvent the rules, but that comes with its own risks.  Police, investigations, prison.  There are other ways, more insulated, which are to play assist to help those people.  Helping them to disappear, cleaning up messes, escrow services for the handling of good, payment, or guests.  Always keeping it professional, keeping things insulated, with layers of distance.  When others panic, with too many variables to consider in the heat of the moment, they can do the thinking.  Who would suspect this mom and dad with two kids?
""".strip()
TOC_URL = "https://clawwebserial.blog/table-of-contents/"


class SourceClaw(BaseSource):
    id = "Claw"
    aliases = ["ClawSerial"]
    title = "Claw"
    authors = ["Wildbow"]
    url = "https://clawwebserial.blog/"
    genres = [
        "Thriller",
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
    return SourceClaw
