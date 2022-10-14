from .base_source import BaseSource, Chapter, SectionedChapterList

DESCRIPTION = """
The Empire stands triumphant.

For twenty years the Dread Empress has ruled over the lands that were once the Kingdom of Callow, but behind the scenes of this dawning golden age threats to the crown are rising. The nobles of the Wasteland, denied the power they crave, weave their plots behind pleasant smiles. In the north the Forever King eyes the ever-expanding borders of the Empire and ponders war. The greatest danger lies to the west, where the First Prince of Procer has finally claimed her throne: her people sundered, she wonders if a crusade might not be the way to secure her reign. Yet none of this matters, for in the heart of the conquered lands the most dangerous man alive sat across an orphan girl and offered her a knife.

Her name is Catherine Foundling, and she has a plan.
""".strip()
TOC_URL = "https://practicalguidetoevil.wordpress.com/table-of-contents"


class SourcePracticalGuideToEvil(BaseSource):
    id = "PracticalGuideToEvil"
    aliases = ["APracticalGuideToEvil", "PGtE"]
    title = "A Practical Guide to Evil"
    authors = ["ErraticErrata"]
    url = "https://practicalguidetoevil.wordpress.com"
    genres = [
        "Adventure",
        "Anti-Hero",
        "Coming of Age",
        "Fantasy",
        "Magic",
        "Young Adult",
    ]
    description = DESCRIPTION
    toc_url = TOC_URL

    def fetch_chapter_list(self) -> SectionedChapterList:
        soup = self.get_soup(TOC_URL)
        toc_html = soup.select_one("div.entry-content")

        structure: SectionedChapterList = []
        for i, ele in enumerate(toc_html.select("div > ul"), start=1):
            structure.append(
                (
                    f"Book {i}",
                    [
                        Chapter(self, a.text, a["href"])
                        for a in ele.select("li > a:not(.share-icon)")
                    ],
                )
            )
        return structure

    def parse_chapter(self, chapter: Chapter, content_raw: str | None = None) -> str:
        soup = self.get_soup(chapter.url, content_raw)
        body = soup.select_one("div.entry-content")
        cleaned = [f"<h2>{chapter.title}</h2>"]
        for tag in body.children:
            if tag.name == "div":
                break
            cleaned.append(str(tag))

        return "\n".join(cleaned)


def get_class() -> type[BaseSource]:
    return SourcePracticalGuideToEvil
