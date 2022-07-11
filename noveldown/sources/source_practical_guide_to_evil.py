from .base_source import BaseSource, Chapter

DESCRIPTION = """
The Empire stands triumphant.

For twenty years the Dread Empress has ruled over the lands that were once the Kingdom of Callow, but behind the scenes of this dawning golden age threats to the crown are rising. The nobles of the Wasteland, denied the power they crave, weave their plots behind pleasant smiles. In the north the Forever King eyes the ever-expanding borders of the Empire and ponders war. The greatest danger lies to the west, where the First Prince of Procer has finally claimed her throne: her people sundered, she wonders if a crusade might not be the way to secure her reign. Yet none of this matters, for in the heart of the conquered lands the most dangerous man alive sat across an orphan girl and offered her a knife.

Her name is Catherine Foundling, and she has a plan.
""".strip()
TOC_URL = "https://practicalguidetoevil.wordpress.com/table-of-contents"


class SourcePracticalGuideToEvil(BaseSource):
    id = "PracticalGuideToEvil"
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

    def fetch_chapter_list(self) -> list[tuple[str, list[Chapter]]]:
        soup = self.get_soup(TOC_URL)
        toc_html = soup.select("div.entry-content")

        structure: list[tuple[str, list[Chapter]]] = []
        active_chapter = ""
        for ele in toc_html:
            if ele.name == "h2":
                active_chapter = ele.text
            elif ele.name == "ul":
                structure.append(
                    (
                        active_chapter,
                        [Chapter(self, a.text, a["href"]) for a in ele],
                    )
                )
        return structure

    def parse_chapter(self, chapter: Chapter) -> str:
        soup = self.get_soup(chapter.url)
        body = soup.select_one("div.entry_content")
        return str(body)


def get_class() -> type[BaseSource]:
    return SourcePracticalGuideToEvil
