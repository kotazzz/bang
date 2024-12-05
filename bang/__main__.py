
import attr
import questionary
from rich.console import Console
from bang.cards import base_cards
from bang.core.commands import give_card
from bang.core.core import Character, Player
from bang.core.deck_master import CardDeck, ShopDeck, create_decks
from bang.core.events import CommandManager, Event, EventHandler, listener

@attr.s(auto_attribs=True)
class Game:
    players: list[Player]
    deck: CardDeck
    shop: ShopDeck
    current: int = 0
    
    events: EventHandler = attr.ib(init=False)
    commands: CommandManager = attr.ib(init=False)
    console: Console = attr.ib(init=False)
    def __attrs_post_init__(self):
        self.events = EventHandler()
        self.commands = CommandManager(self.events)
        self.console = Console()
        
        @self.events.subscribe
        @listener(Event)
        def liste(event: Event):
            self.print(event)
    
    @property
    def exec(self):
        return self.commands.execute
    
    @property
    def print(self):
        return self.console.print
    
    
    def play(self):
        for p in self.players:
            p.hp = p.character.max_hp
            self.exec(give_card(self.deck, p, p.hp))
        while True:
            print(f"Current: {self.current}")
            test = questionary.select("Test", ["a", "b"]).ask()
            print(test)
            
            if test is None:
                print("Bruh")
                break
            
            
            
            

if __name__ == "__main__":
    c, s = create_decks()
    p1 = Player(Character())
    p2 = Player(Character())
    g = Game([p1, p2], c, s)
    g.play()