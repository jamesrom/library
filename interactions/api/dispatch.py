from asyncio import AbstractEventLoop, get_event_loop
from typing import Any, Callable, Coroutine, Optional


class Listener:
    """
    A class representing how events become dispatched and listened to.

    :ivar loop: The coroutine event loop established on.
    :ivar events: A list of events being dispatched.
    """

    __slots__ = ("loop", "events")
    loop: AbstractEventLoop
    events: dict

    def __init__(self, loop: Optional[AbstractEventLoop] = None) -> None:
        """
        :param loop: The coroutine event loop for dispatching.
        :type loop: typing.Optional[asyncio.AbstractEventLoop]
        :return: None
        """
        self.loop = get_event_loop() if loop is None else loop
        self.events = {}

    def dispatch(self, name: str, *args, **kwargs) -> None:
        r"""
        Dispatches an event given out by the gateway.

        :param name: The name of the event to dispatch.
        :type name: str
        :param \*args: Multiple arguments of the coroutine.
        :type \*args: typing.list[typing.Any]
        :param \**kwargs: Keyword-only arguments of the coroutine.
        :type \**kwargs: dict
        :return: None
        """
        for event in self.events.get(name, []):
            self.loop.create_task(event(*args, **kwargs))

    def register(self, coro: Coroutine, name: Optional[str] = None) -> Callable[..., Any]:
        """
        Registers a given coroutine as an event to be listened to.
        If the name of the event is not given, it will then be
        determined by the coroutine's name.

        i.e.:
            async def on_guild_create -> "ON_GUILD_CREATE" dispatch.

        :param coro: The coroutine to register as an event.
        :type coro: typing.Coroutine
        :return: None
        """
        _name: str = coro.__name__ if name is None else name
        event = self.events.get(_name, [])
        event.append(coro)

        self.events[_name] = event
        print(self.events)
