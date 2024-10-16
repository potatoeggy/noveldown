import noveldown

from common import do_first_chapters_content_match, skip_in_ci

OP1 = """<h2>0.0</h2>\n<p>Louise’s eyes welled with moisture as an animal cry shook her house, and she found herself shivering as it died away."""
ED1 = """<p>Dutifully, she put that thought out of mind, as per the terms of the deal she no longer remembered making.</p>"""


@skip_in_ci
def test_pale() -> None:
    source = noveldown.query("pale")
    return do_first_chapters_content_match(source, [("0.0", OP1, ED1)])
