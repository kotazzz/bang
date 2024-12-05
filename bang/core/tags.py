
from collections import defaultdict
from enum import StrEnum, auto
from typing import Callable

from bang.core.core import Card


class Tags(StrEnum):
    DAMAGE = auto()

tagged = defaultdict(list)

def tag(*tags: Tags) -> Callable[..., Card]:
    def decorator(card: Card) -> Card:
        tagged[card].extend(tags)
        return card
    return decorator
    