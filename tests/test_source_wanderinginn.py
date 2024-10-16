import noveldown

from common import do_first_chapters_content_match, skip_in_ci

OP1 = """<h2>1.00</h2>\n\n\n<p>The inn was dark and empty when the traveller arrived. It appeared suddenly, rising above the gentle hills and valleys of autumnal grass that blew in the wind"""
ED1 = """<p>In the darkness, the girl cracked one eye open. She looked around and then sat up.</p>\n\n\n<p>“…What was that?”</p>\n\n\n<p>\xa0</p>\n\n"""


@skip_in_ci
def test_wanderinginn() -> None:
    source = noveldown.query("wanderinginn")
    return do_first_chapters_content_match(source, [("1.00", OP1, ED1)])
