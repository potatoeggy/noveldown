import noveldown

from common import do_first_chapters_content_match, skip_in_ci

OP1 = """<h2>1.1</h2>\n<p>The mountains and hills just outside Camrose were still burning enough that licks of flame pierced the haze of dingy"""
ED1 = """to be a part of it.\xa0 The practice I’ve been doing in my head will help me help you understand.<br/>\n</em></p>"""


@skip_in_ci
def test_claw() -> None:
    source = noveldown.query("claw")
    return do_first_chapters_content_match(source, [("1.1", OP1, ED1)])
