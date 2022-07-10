import sys
import types

from .base_source import BaseSource

from . import (  # isort: skip
    source_practical_guide_to_evil,
    source_wandering_inn,
)

__class_list: list[type[BaseSource]] = []


def _get_all_source_modules() -> list[str]:
    out = []
    for _, val in globals().items():
        if isinstance(val, types.ModuleType) and val.__name__.startswith(
            "noveldown.sources.source_"
        ):
            out.append(val.__name__)
    return out


for i in _get_all_source_modules():
    __class_list.append(sys.modules[i].get_class())


def get_class_for(novel_id: str) -> type[BaseSource]:
    """
    Return a source that matches the ID.
    """
    for c in __class_list:
        if c.check_url(novel_id):
            return c
    raise ValueError("No sources found matched the ID query.")


def get_all_classes() -> list[type[BaseSource]]:
    """
    Return all imported source module classes. Best used for manual poking.
    """
    return __class_list
