from .base_source import BaseSource, Chapter

DESCRIPTION = """
“No killing Goblins.”

So reads the sign outside of The Wandering Inn, a small building run by a young woman named Erin Solstice. She serves pasta with sausage, blue fruit juice, and dead acid flies on request. And she comes from another world. Ours.

It's a bad day when Erin finds herself transported to a fantastical world and nearly gets eaten by a Dragon. She doesn’t belong in a place where monster attacks are a fact of life, and where Humans are one species among many. But she must adapt to her new life. Or die.

In a dangerous world where magic is real and people can level up and gain classes, Erin Solstice must battle somewhat evil Goblins, deadly Rock Crabs, and hungry [Necromancers]. She is no warrior, no mage. Erin Solstice runs an inn.

She's an [Innkeeper].
""".strip()

COVER_URL = "https://m.media-amazon.com/images/I/41zGUBv9XHL.jpg"
TOC_URL = "https://wanderinginn.com/table-of-contents/"


class SourceWanderingInn(BaseSource):
    id = "WanderingInn"
    aliases = ["TheWanderingInn", "TWI"]
    title = "The Wandering Inn"
    authors = ["pirateaba"]
    url = "https://wanderinginn.com"
    genres = [
        "Fantasy",
        "Fiction",
        "Adventure",
        "Young Adult",
        "Magic",
    ]
    description = DESCRIPTION
    cover_url = COVER_URL

    def fetch_chapter_list(self) -> list[Chapter]:
        soup = self.get_soup(TOC_URL)
        toc_html = soup.select("div.entry-content a")

        return [Chapter(self, el.text, el["href"]) for el in toc_html]

    def parse_chapter(self, chapter: Chapter, content_raw: str | None = None) -> str:
        soup = self.get_soup(chapter.url, content_raw)
        body = soup.select_one("div.entry-content")
        cleaned = [f"<h2>{chapter.title}</h2>"]

        for tag in body.children:
            if tag.name == "hr" or tag.name == "div":
                break
            cleaned.append(str(tag))

        return "\n".join(cleaned)


def get_class() -> type[BaseSource]:
    return SourceWanderingInn
