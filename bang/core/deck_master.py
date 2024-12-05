

from random import shuffle
from typing import Callable, Type
import attr
from bang.core.core import Card, Equipment





@attr.s(auto_attribs=True)
class Deck[T]:
    cards: list[T]
    used: list[T] = attr.ib(factory=list)
    
    @property
    def pop(self) -> T:
        return self.cards.pop
    
    def reshuffle(self):
        shuffle(self.used)
        self.cards.extend(self.used)
        self.used.clear()

class CardDeck(Deck[Card]):
    pass

class ShopDeck(Deck[Equipment]):
    @property
    def active(self) -> list[Equipment]:
        return self.cards[-3:]

cards: list[tuple[Card, int]] = []
equipment: list[tuple[Equipment, int]] = []

def register_card(count: int = 1)  -> Callable[..., Card | Equipment]:
    def decorator(item: Type[Card | Equipment])  -> Card | Equipment:
        if isinstance(item, Card):
            cards.append((item, count))
        else:
            equipment.append((item, count))
        return item
    return decorator

def create_decks() -> tuple[CardDeck, ShopDeck]:
    cards_deck = []
    for card, count in cards:
        for _ in range(count):
            cards_deck.append(card)
            
    eq_deck = []
    for eq, count in equipment:
        for _ in range(count):
            eq_deck.append(eq)
    
    shuffle(cards_deck)
    shuffle(eq_deck)
    return CardDeck(cards=cards_deck), ShopDeck(cards=eq_deck)