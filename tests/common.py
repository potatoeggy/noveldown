import os

import pytest

from noveldown.sources import BaseSource

skip_in_ci = pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS") == "true", reason="Do not run network tests in CI"
)

ChapterExpectation = tuple[str, str, str]  # title, startswith, endswith


def do_first_chapters_content_match(
    source: BaseSource, expectation: list[ChapterExpectation]
) -> None:
    assert len(source.chapters_flattened) >= len(expectation)
    for chap, (title, startswith, endswith) in zip(source.chapters_flattened, expectation):
        assert chap.title == title, f"Got: {chap.title}"
        assert chap.content.startswith(startswith), f"Got: {repr(chap.content[:len(startswith)])}"
        assert chap.content.endswith(endswith), f"Got: {repr(chap.content[-len(endswith):])}"
