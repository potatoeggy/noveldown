import noveldown

from common import do_first_chapters_content_match, skip_in_ci

OP1 = """<h2>Prologue</h2>\n\n\n<p><span style="font-size:medium;"><em>In the beginning, there were only the Gods</em>.</span><br/>\n<span style="font-size:medium;"><i>Aeons untold passed as they drifted aimlessly"""
ED1 = """The Dread Empire of Praes may have won the war, but the clock was already ticking. The Legions of Terrors had made a lot of angry orphans through the afternoon’s bloody work, and in time that would mean one thing –</span></p>\n\n\n<p><span style="font-size:medium;">Heroes.</span></p>\n\n"""


@skip_in_ci
def test_practical_guide_to_evil() -> None:
    source = noveldown.query("practical_guide_to_evil")
    return do_first_chapters_content_match(source, [("Prologue", OP1, ED1)])
