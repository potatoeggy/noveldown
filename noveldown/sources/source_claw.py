from .source_pale import SourcePale
from .base_source import BaseSource

DESCRIPTION = """
Joshua Munce, Sheila Hardy, Dan Whitely, Max Highland, Tonya Keifer, Marvin Su… this pair has many names, but those names aren’t their own; they’re names to sell.  In a rigged and crumbling system, the only way to get ahead is to circumvent the rules, but that comes with its own risks.  Police, investigations, prison.  There are other ways, more insulated, which are to play assist to help those people.  Helping them to disappear, cleaning up messes, escrow services for the handling of good, payment, or guests.  Always keeping it professional, keeping things insulated, with layers of distance.  When others panic, with too many variables to consider in the heat of the moment, they can do the thinking.  Who would suspect this mom and dad with two kids?
""".strip()
TOC_URL = "https://clawwebserial.blog/table-of-contents/"


class SourceClaw(SourcePale):
    id = "Claw"
    aliases = ["ClawSerial"]
    title = "Claw"
    authors = ["Wildbow"]
    url = "https://clawwebserial.blog/"
    genres = [
        "Thriller",
    ]
    description = DESCRIPTION
    toc_url = TOC_URL


def get_class() -> type[BaseSource]:
    return SourceClaw
