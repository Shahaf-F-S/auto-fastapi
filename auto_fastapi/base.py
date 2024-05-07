# base.py

from dataclasses import dataclass, field
from abc import ABCMeta

from fastapi import FastAPI, APIRouter

__all__ = [
    "BaseEndpoints",
    "EndpointsRouter"
]

class BaseEndpoints(metaclass=ABCMeta):

    pass

@dataclass
class EndpointsRouter[T: BaseEndpoints]:

    router: FastAPI | APIRouter
    endpoints: T = None
    routers: list["EndpointsRouter"] = field(default_factory=list)

    def include(self) -> None:

        for router in self.routers:
            self.router.include_router(router.router)

    def select[T: BaseEndpoints](self, base: type[T]) -> "EndpointsRouter[T]":

        for router in self.routers:
            if isinstance(router.endpoints, base):
                return router
