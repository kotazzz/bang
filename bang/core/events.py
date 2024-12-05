from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Generator

import attr

type EventType = type[Event]
type Callback = Callable[[Event], None]
type CommandCallback = Callable[..., Generator[Event, Any, Any]]



def command(callback: CommandCallback) -> Command:
    return Command(callback=callback)

@attr.s(auto_attribs=True)
class Listener:
    event: EventType
    callback: Callback


class Event:
    pass


def listener(event: EventType) -> Callable[..., Listener]:
    def decorator(callback: Callback) -> Listener:
        return Listener(event, callback)

    return decorator


class EventHandler:
    def __init__(self, *lookup: object) -> None:
        self.listeners: dict[EventType, list[Listener]] = defaultdict(list)
        for obj in lookup:
            self.lookup(obj)

    def subscribe(self, callback: Listener) -> None:
        if callback not in self.listeners[callback.event]:
            self.listeners[callback.event].append(callback)

    def lookup(self, obj: object) -> None:
        for attrib in dir(obj):
            item = getattr(obj, attrib)
            if isinstance(item, Listener):
                self.subscribe(item)

    def publish(self, event: Event) -> None:
        for listener in self.listeners[type(event)]:
            listener.callback(event)

        for listener in self.listeners[Event]:
            listener.callback(event)

    def __repr__(self) -> str:
        return f"<EventHandler listeners={len(self.listeners)}>"


@attr.s(auto_attribs=True)
class Command:
    callback: CommandCallback
    args: tuple[Any, ...] = attr.ib(factory=tuple)
    kwargs: dict[str, Any] = attr.ib(factory=dict)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.args = args
        self.kwargs = kwargs
        return self


class CommandManager:
    def __init__(self, event_handler: EventHandler) -> None:
        self.event_handler = event_handler

    def execute(self, command: Command) -> Any | None:
        a, k = command.args, command.kwargs
        gen = command.callback(*a, **k)
        for event in gen:
            self.event_handler.publish(event)
        try:
            next(gen)
        except StopIteration as e:
            return e.value
        return None
