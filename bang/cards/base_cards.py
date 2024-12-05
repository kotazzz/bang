import attr
from bang.core.core import Card, CardType, Player, create_card
from bang.core.deck_master import register_card
from bang.core.events import Event, command
from bang.core.tags import Tags, tag, tagged

@attr.s(auto_attribs=True)
class Damage(Event):
    card: Card
    target: Player

@attr.s(auto_attribs=True)
class Cancel(Event):
    target: Player

@register_card(5)
@tag(Tags.DAMAGE)
@create_card("Бэнг!", "Нанесите урон противнику!", CardType.OPPONENT)
@command
def bang_command(card: Card, caller: Player, target: Player):
    yield Damage(card, target)

@register_card(5)
@create_card("Мимо!", "Неа, мимо!", CardType.REPLY)
@command
def miss_command(card: Card, caller: Player):
    if Tags.DAMAGE in tagged[card]:
        yield Cancel(caller)
 