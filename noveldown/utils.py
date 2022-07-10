import imghdr
import io
from pathlib import Path

import requests
from ebooklib import epub

from .sources.base_source import BaseSource, Chapter

STYLE_CSS = """
body { background-color: #ffffff;
text-align: justify;
margin: 2%;
adobe-hyphenate: none; }
pre { font-size: x-small; }
h1 { text-align: center; }
h2 { text-align: center; }
h3 { text-align: center; }
h4 { text-align: center; }
h5 { text-align: center; }
h6 { text-align: center; }
.CI {
text-align:center;
margin-top:0px;
margin-bottom:0px;
padding:0px;
}
.center   {text-align: center;}
.cover    {text-align: center;}
.full     {width: 100%; }
.quarter  {width: 25%; }
.smcap    {font-variant: small-caps;}
.u        {text-decoration: underline;}
.bold     {font-weight: bold;}
.big { font-size: larger; }
.small { font-size: smaller; }
"""


def create_epub(source: BaseSource, path: Path | str) -> None:
    path = Path(path)

    book = epub.EpubBook()
    book.set_identifier(source.id)
    book.set_title(source.title)
    book.set_language("en")

    book.add_metadata("dc", "description", source.description)
    book.add_metadata("dc", "contributor", "noveldown")
    book.add_metadata("dc", "source", source.url)
    for genre in source.genres:
        book.add_metadata("dc", "subject", genre)

    for author in source.authors:
        book.add_author(author)

    chapter_htmls: list[epub.EpubHtml] = []
    # assume there is at least one chapter
    if isinstance(source.chapters[0], Chapter):
        for i, chap in enumerate(source.chapters):
            # get mypy to stop yelling at me even though it's slow
            assert isinstance(chap, Chapter)
            chapter_htmls.append(
                epub.EpubHtml(
                    file_name=f"{i}.xhtml",
                    title=chap.title,
                    lang="en",
                    content=chap.content,
                )
            )
    else:
        for i, section in enumerate(source.chapters):
            assert isinstance(section, tuple)
            _, chapters = section
            for j, chap in enumerate(chapters):
                assert isinstance(chap, Chapter)
                chapter_htmls.append(
                    epub.EpubHtml(
                        file_name=f"{i}-{j}.xhtml",
                        title=chap.title,
                        lang="en",
                        content=chap.content,
                    )
                )

    style = epub.EpubItem(
        uid="style", file_name="style.css", media_type="text/css", content=STYLE_CSS
    )
    book.add_item(style)

    book.spine = ["nav", *chapter_htmls]
    if source.cover_url:
        image = requests.get(source.cover_url).content
        ext = imghdr.what(io.BytesIO(image))
        book.set_cover(f"cover.{ext}", image)
        book.spine.insert(0, "cover")

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(str(path / f"{source.title}.epub"), book, {})
