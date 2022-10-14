import asyncio
import imghdr
import io
from pathlib import Path
from typing import AsyncIterator, Iterator, cast

import httpx
import requests
from ebooklib import epub

from .sources.base_source import BaseSource, Chapter, SectionedChapterList

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

MAX_DEFAULT_THREADS = 16


async def magic(
    source: BaseSource, threads: int = MAX_DEFAULT_THREADS
) -> AsyncIterator[str]:
    limits = httpx.Limits(
        max_connections=threads, max_keepalive_connections=threads, keepalive_expiry=5
    )
    async with httpx.AsyncClient(limits=limits) as client:
        functions = [chap.get_raw_content(client) for chap in source.chapters_flattened]

        for result in asyncio.as_completed(functions):
            yield await result


def load_all_chapters(
    source: BaseSource, threads: int = MAX_DEFAULT_THREADS
) -> Iterator[str]:
    """
    Calls the property for each chapter to collect them all
    in memory asynchronously to be extra fast.
    """
    gen = magic(source, threads)
    loop = asyncio.get_event_loop()
    while True:
        try:
            yield loop.run_until_complete(gen.__anext__())
        except StopAsyncIteration:
            break


def create_epub(source: BaseSource, path: Path | str) -> Iterator[str]:
    # TODO: split this into multiple functions (iohandler?) and add threads
    path = Path(path)

    book = epub.EpubBook()
    book.set_identifier(source.id)
    book.set_title(source.title)
    book.set_language("en")

    book.add_metadata("DC", "description", source.description)
    book.add_metadata("DC", "contributor", "noveldown")
    book.add_metadata("DC", "source", source.url)
    book.add_metadata("DC", "publisher", source.url)
    for genre in source.genres:
        book.add_metadata("DC", "subject", genre)

    for author in source.authors:
        book.add_author(author)

    style = epub.EpubItem(
        uid="style", file_name="style.css", media_type="text/css", content=STYLE_CSS
    )
    book.add_item(style)

    chapter_htmls: list[epub.EpubHtml] = []

    # assume there is at least one chapter
    if isinstance(source.chapters[0], Chapter):
        for i, chap in enumerate(source.chapters):
            # get mypy to stop yelling at me even though it's slow
            chap = cast(Chapter, chap)
            draft = epub.EpubHtml(
                file_name=f"{i}.xhtml",
                title=chap.title,
                lang="en",
                content=chap.content,
            )
            draft.add_item(style)
            chapter_htmls.append(draft)
            yield chap.title
        book.toc = [*chapter_htmls]
    else:
        book.toc = []
        for i, section in enumerate(cast(SectionedChapterList, source.chapters)):
            sec_title, chapters = section
            book.toc.append((epub.Section(sec_title), []))

            for j, chap in enumerate(chapters):
                draft = epub.EpubHtml(
                    file_name=f"{i}-{j}.xhtml",
                    title=chap.title,
                    lang="en",
                    content=chap.content,
                )
                draft.add_item(style)
                chapter_htmls.append(draft)
                book.toc[i][1].append(draft)
                yield f"{sec_title} - {chap.title}"

    for i in chapter_htmls:
        book.add_item(i)

    book.spine = [*chapter_htmls]
    if source.cover_url:
        image = requests.get(source.cover_url).content
        ext = imghdr.what(io.BytesIO(image))
        book.set_cover(f"cover.{ext}", image)
        book.spine.insert(0, "cover")

    book.add_item(epub.EpubNcx())

    dest_file = path / f"{source.title}.epub"
    epub.write_epub(str(dest_file), book, {})
