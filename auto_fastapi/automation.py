# automation.py

import asyncio
from dataclasses import dataclass, field
from typing import Callable, Awaitable
from functools import partial

from dataplace import Callback

from auto_fastapi.base import EndpointsRouter

__all__ = [
    "Automation"
]

@dataclass
class Automation:

    operation: Callable[[EndpointsRouter], ... | Awaitable]

    complete: bool = False
    running: bool = False

    callback: Callback = field(init=False, default=None)
    automations: list["Automation"] = field(default_factory=list)

    def __post_init__(self) -> None:

        self.callback = self.create_callback()

    def create_callback(self) -> Callback:

        return Callback(self.operation, types={EndpointsRouter})

    def support(self, *args, **kwargs) -> "Automation":

        automation = Automation(*args, **kwargs)
        automation.automations.insert(0, self)

        return automation

    @staticmethod
    def supports(*automations, **kwargs) -> Callable[..., "Automation"]:

        return partial(
            Automation(lambda _: (), automations=list(automations)).support,
            **kwargs
        )

    def automate(self, router: EndpointsRouter) -> None:

        if self.complete:
            return

        self.running = True
        self.complete = False

        for automation in self.automations:
            automation.automate(router)

        self.callback.call(router)

        self.running = False
        self.complete = True

    async def async_automate(self, router: EndpointsRouter) -> None:

        if self.complete:
            return

        self.running = True
        self.complete = False

        await asyncio.gather(
            automation.async_automate(router)
            for automation in self.automations
        )

        await self.callback.async_call(router)

        self.running = False
        self.complete = True

    def copy(
            self,
            deep: bool = False,
            separate: bool = True,
            complete: bool = None
    ) -> "Automation":

        automations = self.automations

        if separate and not deep:
            automations = automations.copy()

        elif deep:
            automations = [
                automation.copy(deep=deep, separate=False, complete=complete)
                for automation in automations
            ]

        return Automation(
            operation=self.operation,
            automations=automations,
            complete=self.complete if complete is None else complete
        )

    def clear(self) -> None:

        self.complete = False
