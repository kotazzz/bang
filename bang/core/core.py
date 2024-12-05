from enum import StrEnum, auto
from typing import Callable
import attr

from bang.core.events import Command

class CardType(StrEnum):
    ALL = auto()
    SELF = auto()
    OPPONENT = auto()
    SAVE = auto()
    DELAY = auto()
    REPLY = auto()

class Role(StrEnum): 
    SHERIFF = auto()
    BANDIT = auto()
    RENEGADE = auto()

@attr.s(auto_attribs=True)
class Character:
    max_hp: int = 4
    # name, desc
    # effect: Command
    
@attr.s(auto_attribs=True, frozen=True)
class Card:
    use: Command = attr.ib(hash=False)
    name: str = "Карта без имени"
    description: str = "Карта без имени"
    use_type: CardType = CardType.OPPONENT
    

def create_card(name: str,description: str,use_type: CardType)-> Callable[..., Card]:
    def card(command: Command) -> Card:
        return Card(command, name, description, use_type)
    return card

@attr.s(auto_attribs=True)
class Equipment(Card):
    dissolve: bool = True
    cost: int = 1

@attr.s(auto_attribs=True)
class Player:
    character: Character
    # role: None
    hand: list[Card] = attr.ib(factory=list)
    activate: list[Card] = attr.ib(factory=list)
    equip: list[Equipment] = attr.ib(factory=list)
    gold: int = 0
    hp: int = 0

