from __future__ import annotations

from typing import TYPE_CHECKING
import attr

from bang.core.core import Card, Player
from bang.core.deck_master import CardDeck
from bang.core.events import Event, command

if TYPE_CHECKING:
    from bang.__main__ import Game
    
@attr.s(auto_attribs=True)
class CardRecieve(Event):
    player: Player
    count: int
    
    
@attr.s(auto_attribs=True)
class EndMove(Event):
    player: Player

@command
def give_card(deck: CardDeck, player: Player, count: int):
    for _ in range(count):
        player.hand.append(deck.pop())
    yield CardRecieve(player, count)

@command
def use_card(game: Game, player: Player, card: Card):
    pass

@command
def end_move(game: Game, player: Player):
    game.current += 1
    yield EndMove(player)