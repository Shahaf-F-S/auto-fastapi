# auto.py

from abc import ABCMeta
from enum import Enum
from dataclasses import dataclass
from typing import Sequence, Callable, overload, Iterable, Self, TypeVar

from fastapi import Response, Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.datastructures import Default
from fastapi.utils import generate_unique_id
from fastapi.routing import APIRoute, BaseRoute

__all__ = [
    "BaseEndpoint",
    "Endpoint",
    "EndpointBuilder",
    "bind",
    "Method",
    "METHODS",
    "BoundEndpoint",
    "add",
    "bind_endpoint",
    "bind_event",
    "add_event",
    "add_endpoint",
    "AddedEvent",
    "AddedEndpoint",
    "add_websocket_endpoint",
    "bind_websocket_endpoint",
    "build_endpoint",
    "build_websocket_endpoint",
    "add_all",
    "WebSocketEndpoint",
    "AddedWebSocketEndpoint",
    "BoundWebSocketEndpoint",
    "add_exception_handler",
    "add_middleware",
    "bind_exception_handler",
    "bind_middleware",
    "build_middleware",
    "build_exception_handler",
    "Middleware",
    "BoundMiddleware",
    "AddedMiddleware",
    "ExceptionHandler",
    "BoundExceptionHandler",
    "AddedExceptionHandler",
    "clone",
    "clone_all",
    "Event",
    "BoundEvent",
    "BOUND",
    "BUILT",
    "ADDED",
    "AutoFasAPI",
    "bind_all",
    "Builder"
]

IncEx = set[int] | set[str] | dict[int, ...] | dict[str, ...]

class Method(Enum):

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    UPLOAD = "UPLOAD"
    HEAD = "HEAD"
    PATCH = "PATCH"
    PUT = "PUT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"

METHODS = (
    Method.GET, Method.POST, Method.DELETE, Method.UPLOAD,
    Method.HEAD, Method.PATCH, Method.PUT, Method.OPTIONS,
    Method.TRACE
)

@dataclass(slots=True)
class WebSocketEndpoint:

    path: str
    name: str = None
    dependencies: Sequence[Depends] = None

    def data(self) -> dict[str, ...]:

        return dict(
            path=self.path,
            name=self.name,
            dependencies=self.dependencies
        )

    def clone(self) -> Self:

        return WebSocketEndpoint(**self.data())

    def bind(self, c: Callable) -> "BoundWebSocketEndpoint":

        return BoundWebSocketEndpoint(c=c, endpoint=self)

@dataclass(slots=True)
class BoundWebSocketEndpoint:

    c: Callable
    endpoint: WebSocketEndpoint

    def data(self) -> dict[str, ...]:

        return self.endpoint.data()

    def clone(self) -> Self:

        return BoundWebSocketEndpoint(
            c=self.c, endpoint=self.endpoint.clone()
        )

@dataclass(slots=True)
class AddedWebSocketEndpoint:

    bound: BoundWebSocketEndpoint
    added: Callable

@dataclass(slots=True)
class Event:

    event_type: str

    def data(self) -> dict[str, ...]:

        return dict(event_type=self.event_type)

    def clone(self) -> Self:

        return Event(**self.data())

    def bind(self, c: Callable) -> "BoundEvent":

        return BoundEvent(c=c, event=self)

@dataclass(slots=True)
class BoundEvent:

    c: Callable
    event: Event

    def data(self) -> dict[str, ...]:

        return self.event.data()

    def clone(self) -> Self:

        return BoundEvent(c=self.c, event=self.event.clone())

@dataclass(slots=True)
class AddedEvent:

    bound: BoundEvent
    added: Callable

@dataclass(slots=True)
class Middleware:

    middleware_type: str

    def data(self) -> dict[str, ...]:

        return dict(middleware_type=self.middleware_type)

    def clone(self) -> Self:

        return Middleware(**self.data())

    def bind(self, c: Callable) -> "BoundMiddleware":

        return BoundMiddleware(c=c, middleware=self)

@dataclass(slots=True)
class BoundMiddleware:

    c: Callable
    middleware: Middleware

    def data(self) -> dict[str, ...]:

        return self.middleware.data()

    def clone(self) -> Self:

        return BoundMiddleware(
            c=self.c, middleware=self.middleware.clone()
        )

@dataclass(slots=True)
class AddedMiddleware:

    bound: BoundMiddleware
    added: Callable

@dataclass(slots=True)
class ExceptionHandler:

    exc_class_or_status_code: int | type[Exception]

    def data(self) -> dict[str, ...]:

        return dict(exc_class_or_status_code=self.exc_class_or_status_code)

    def clone(self) -> Self:

        return ExceptionHandler(**self.data())

@dataclass(slots=True)
class BoundExceptionHandler:

    c: Callable
    handler: ExceptionHandler

    def data(self) -> dict[str, ...]:

        return self.handler.data()

    def clone(self) -> Self:

        return BoundExceptionHandler(
            c=self.c, handler=self.handler.clone()
        )

@dataclass(slots=True)
class AddedExceptionHandler:

    bound: BoundExceptionHandler
    added: Callable

@dataclass(slots=True)
class BaseEndpoint:

    path: str
    methods: Iterable[Method]
    response_model: ... = None
    status_code: int = None
    tags: list[str | Enum] = None
    dependencies: Sequence[Depends] = None
    summary: str = None
    description: str = None
    response_description: str = "Successful Response"
    responses: dict[int | str, dict[str, ...]] = None
    deprecated: bool = None
    operation_id: str = None
    response_model_include: IncEx = None
    response_model_exclude: IncEx = None
    response_model_by_alias: bool = True
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    include_in_schema: bool = True
    response_class: type[Response] = JSONResponse
    name: str = None
    callbacks: list[BaseRoute] = None
    openapi_extra: dict[str, ...] = None
    generate_unique_id_function: Callable[[APIRoute], str] = None

    def data(self) -> dict[str, ...]:

        return dict(
            path=self.path,
            response_model=self.response_model,
            status_code=self.status_code,
            tags=self.tags,
            dependencies=self.dependencies,
            summary=self.summary,
            description=self.description,
            response_description=self.response_description,
            responses=self.responses,
            deprecated=self.deprecated,
            operation_id=self.operation_id,
            response_model_include=self.response_model_include,
            response_model_exclude=self.response_model_exclude,
            response_model_by_alias=self.response_model_by_alias,
            response_model_exclude_unset=self.response_model_exclude_unset,
            response_model_exclude_defaults=self.response_model_exclude_defaults,
            response_model_exclude_none=self.response_model_exclude_none,
            include_in_schema=self.include_in_schema,
            response_class=self.response_class,
            name=self.name,
            callbacks=self.callbacks,
            openapi_extra=self.openapi_extra,
            generate_unique_id_function=self.generate_unique_id_function
        )

@dataclass(slots=True)
class Endpoint(BaseEndpoint):

    c: Callable = None

    def clone(self) -> Self:

        return Endpoint(c=self.c, **self.data())

@dataclass(slots=True)
class EndpointBuilder(BaseEndpoint):

    def build(self, c: Callable) -> Endpoint:

        return Endpoint(c=c, methods=self.methods, **self.data())

    def clone(self) -> Self:

        return EndpointBuilder(methods=self.methods, **self.data())

@dataclass(slots=True)
class BoundEndpoint:

    c: Callable
    builder: EndpointBuilder
    endpoints: dict[Method, Endpoint]

    def data(self) -> dict[str, ...]:

        return self.builder.data()

    def clone(self) -> Self:

        return BoundEndpoint(
            c=self.c,
            builder=self.builder,
            endpoints=self.endpoints
        )

@dataclass(slots=True)
class AddedEndpoint:

    bound: BoundEndpoint
    added: dict[Method, Callable]

def build_websocket_endpoint(
        path: str,
        name: str = None,
        dependencies: Sequence[Depends] = None
) -> WebSocketEndpoint:

    return WebSocketEndpoint(
        path=path,
        name=name,
        dependencies=dependencies
    )

def build_exception_handler(
        exc_class_or_status_code: int | type[Exception]
) -> ExceptionHandler:

    return ExceptionHandler(
        exc_class_or_status_code=exc_class_or_status_code
    )

def build_middleware(middleware_type: str) -> Middleware:

    return Middleware(middleware_type=middleware_type)

def build_event(event_type: str) -> Event:

    return Event(event_type=event_type)

def build_endpoint(
        path: str,
        methods: Iterable[Method],
        response_model: ... = Default(None),
        status_code: int = None,
        tags: list[str | Enum] = None,
        dependencies: Sequence[Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: dict[int | str, dict[str, ...]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: IncEx = None,
        response_model_exclude: IncEx = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: type[Response] = Default(JSONResponse),
        name: str = None,
        callbacks: list[BaseRoute] = None,
        openapi_extra: dict[str, ...] = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id)
) -> EndpointBuilder:

    return EndpointBuilder(
        path=path,
        methods=methods,
        response_model=response_model,
        status_code=status_code,
        tags=tags,
        dependencies=dependencies,
        summary=summary,
        description=description,
        response_description=response_description,
        responses=responses,
        deprecated=deprecated,
        operation_id=operation_id,
        response_model_include=response_model_include,
        response_model_exclude=response_model_exclude,
        response_model_by_alias=response_model_by_alias,
        response_model_exclude_unset=response_model_exclude_unset,
        response_model_exclude_defaults=response_model_exclude_defaults,
        response_model_exclude_none=response_model_exclude_none,
        include_in_schema=include_in_schema,
        response_class=response_class,
        name=name,
        callbacks=callbacks,
        openapi_extra=openapi_extra,
        generate_unique_id_function=generate_unique_id_function
    )

def bind_endpoint(c: Callable, builder: EndpointBuilder) -> BoundEndpoint:

    return BoundEndpoint(
        c=c,
        builder=builder,
        endpoints={
            method: builder.build(c)
            for method in set(builder.methods)
        }
    )

def bind_event(c: Callable, event: Event) -> BoundEvent:

    return BoundEvent(c=c, event=event)

def bind_websocket_endpoint(
        c: Callable, endpoint: WebSocketEndpoint
) -> BoundWebSocketEndpoint:

    return BoundWebSocketEndpoint(c=c,  endpoint=endpoint)

def bind_exception_handler(
        c: Callable, handler: ExceptionHandler
) -> BoundExceptionHandler:

    return BoundExceptionHandler(c=c,  handler=handler)

def bind_middleware(
        c: Callable, middleware: Middleware
) -> BoundMiddleware:

    return BoundMiddleware(c=c,  middleware=middleware)

@overload
def bind(c: Callable, middleware: Middleware) -> BoundMiddleware:

    pass

@overload
def bind(c: Callable, handler: ExceptionHandler) -> BoundExceptionHandler:

    pass

@overload
def bind(c: Callable, builder: EndpointBuilder) -> BoundEndpoint:

    pass

@overload
def bind(c: Callable, websocket: WebSocketEndpoint) -> BoundWebSocketEndpoint:

    pass

@overload
def bind(c: Callable, endpoint: EndpointBuilder) -> BoundEndpoint:

    pass

@overload
def bind(c: Callable, endpoint: WebSocketEndpoint) -> BoundWebSocketEndpoint:

    pass

@overload
def bind(c: Callable, event: str) -> BoundEvent:

    pass

Bound = (
    BoundEndpoint |
    BoundWebSocketEndpoint |
    BoundEvent |
    BoundExceptionHandler |
    BoundMiddleware
)

BOUND = [
    BoundEndpoint,
    BoundWebSocketEndpoint,
    BoundEvent,
    BoundExceptionHandler,
    BoundMiddleware
]

def bind(c: Callable, *args, **kwargs) -> Bound:

    if (
        (not args and not kwargs) or
        (args and kwargs) or
        (len(args) > 1) or
        (len(kwargs) > 1)
    ):
        raise TypeError(
            f"{bind} can take either two positional "
            "arguments or one positional and one keyword arguments."
        )

    if kwargs:
        key, value = list(kwargs.items())[0]

        if (key == "event") and isinstance(value, Event):
            return bind_event(c, value)

        elif (key in ("builder", "endpoint")) and isinstance(value, EndpointBuilder):
            return bind_endpoint(c, value)

        elif (key in ("websocket", "endpoint")) and isinstance(value, WebSocketEndpoint):
            return bind_websocket_endpoint(c, value)

        elif (key == "middleware") and isinstance(value, Middleware):
            return bind_middleware(c, value)

        elif (key == "handler") and isinstance(value, ExceptionHandler):
            return bind_exception_handler(c, value)

        else:
            raise TypeError(
                f"{bind} keyword argument no.1 must be either "
                f"'event' with a value of type "
                f"{Event} for binding an event by that name, "
                f"('builder' | 'endpoint') with a value of type {EndpointBuilder} "
                f"for binding an endpoint, ('websocket' | 'endpoint') "
                f"with a value of type {WebSocketEndpoint} for binding a "
                f"websocket endpoint, 'middleware' with a "
                f"value of type {Middleware} for binding a middleware, "
                f"or 'handler' with a value of type "
                f"{ExceptionHandler} for binding an exception handler, "
                f"got key: '{key}' and value: {value}"
            )

    if args:
        if isinstance(args[0], Event):
            return bind_event(c, args[0])

        elif isinstance(args[0], EndpointBuilder):
            return bind_endpoint(c, args[0])

        elif isinstance(args[0], WebSocketEndpoint):
            return bind_websocket_endpoint(c, args[0])

        elif isinstance(args[0], Middleware):
            return bind_middleware(c, args[0])

        elif isinstance(args[0], ExceptionHandler):
            return bind_exception_handler(c, args[0])

        else:
            raise TypeError(
                f"{bind} positional argument no.2 must be either of type "
                f"{Event} for binding an event by that name, "
                f"of type {EndpointBuilder} for binding an endpoint, "
                f"of type {WebSocketEndpoint} for binding a websocket endpoint, "
                f"of type {Middleware} for binding a middleware, "
                f"or of type {ExceptionHandler} for binding an exception handler, "
                f"got: {type(args[0])}"
            )

Built = WebSocketEndpoint | EndpointBuilder | Middleware | ExceptionHandler | Event
BUILT = [WebSocketEndpoint, EndpointBuilder, Middleware, ExceptionHandler, Event]

def bind_all(data: Iterable[tuple[Callable, Built]]) -> list[Bound]:

    return [bind(c, built) for c, built in data]

def add_endpoint(app: FastAPI | APIRoute, endpoint: BoundEndpoint) -> AddedEndpoint:

    return AddedEndpoint(
        bound=endpoint,
        added={
            method: getattr(app, method.value.lower())(**endpoint.data())(endpoint.c)
            for method, method_endpoint in endpoint.endpoints.items()
            if hasattr(app, method.value.lower())
        }
    )

def add_websocket_endpoint(
        app: FastAPI | APIRoute, endpoint: BoundWebSocketEndpoint
) -> AddedWebSocketEndpoint:

    return AddedWebSocketEndpoint(
        bound=endpoint,
        added=app.websocket(**endpoint.data())(endpoint.c)
    )

def add_middleware(
        app: FastAPI | APIRoute, middleware: BoundMiddleware
) -> AddedMiddleware:

    return AddedMiddleware(
        bound=middleware,
        added=app.middleware(**middleware.data())(middleware.c)
    )

def add_exception_handler(
        app: FastAPI | APIRoute, handler: BoundExceptionHandler
) -> AddedExceptionHandler:

    return AddedExceptionHandler(
        bound=handler,
        added=app.exception_handler(**handler.data())(handler.c)
    )

def add_event(app: FastAPI | APIRoute, event: BoundEvent) -> AddedEvent:

    return AddedEvent(
        bound=event,
        added=app.on_event(**event.data())(event.c)
    )

@overload
def add(app: FastAPI | APIRoute, endpoint: BoundEndpoint) -> AddedEndpoint:

    pass

@overload
def add(
        app: FastAPI | APIRoute, endpoint: BoundWebSocketEndpoint
) -> AddedWebSocketEndpoint:

    pass

@overload
def add(
        app: FastAPI | APIRoute, websocket: BoundWebSocketEndpoint
) -> AddedWebSocketEndpoint:

    pass

@overload
def add(app: FastAPI | APIRoute, event: BoundEvent) -> AddedEvent:

    pass

Added = (
    AddedEndpoint |
    AddedWebSocketEndpoint |
    AddedEvent |
    AddedMiddleware |
    AddedExceptionHandler
)

ADDED = [
    AddedEndpoint,
    AddedWebSocketEndpoint,
    AddedEvent,
    AddedMiddleware,
    AddedExceptionHandler
]

App = FastAPI | APIRoute

def add(app: App, *args, **kwargs) -> Added:

    if (
        (not args and not kwargs) or
        (args and kwargs) or
        (len(args) > 1) or
        (len(kwargs) > 1)
    ):
        raise TypeError(
            f"{add} can take either two positional "
            "arguments or one positional and one keyword arguments."
        )

    if kwargs:
        key, value = list(kwargs.items())[0]

        if (key == "event") and isinstance(value, BoundEvent):
            return add_event(app, value)

        elif (key == "endpoint") and isinstance(value, BoundEndpoint):
            return add_endpoint(app, value)

        elif (
            (key in ("websocket", "endpoint")) and
            isinstance(value, BoundWebSocketEndpoint)
        ):
            return add_websocket_endpoint(app, value)

        elif (key == "middleware") and isinstance(value, BoundMiddleware):
            return add_middleware(app, value)

        elif (key == "handler") and isinstance(value, BoundExceptionHandler):
            return add_exception_handler(app, value)

        else:
            raise TypeError(
                f"{bind} keyword argument no.1 must be either "
                f"'event' with a value of type "
                f"{str} for adding an event by that name, "
                f"('builder' | 'endpoint') with a value of type {EndpointBuilder} "
                f"for adding an endpoint, ('websocket' | 'endpoint') "
                f"with a value of type {WebSocketEndpoint} for adding a "
                f"websocket endpoint, 'middleware' with a "
                f"value of type {Middleware} for adding a middleware, "
                f"or 'handler' with a value of type "
                f"{ExceptionHandler} for adding an exception handler, "
                f"got key: '{key}' and value: {value}"
            )

    if args:
        if isinstance(args[0], BoundEvent):
            return add_event(app, args[0])

        elif isinstance(args[0], BoundEndpoint):
            return add_endpoint(app, args[0])

        elif isinstance(args[0], BoundWebSocketEndpoint):
            return add_websocket_endpoint(app, args[0])

        elif isinstance(args[0], BoundMiddleware):
            return add_middleware(app, args[0])

        elif isinstance(args[0], BoundExceptionHandler):
            return add_exception_handler(app, args[0])

        else:
            raise TypeError(
                f"{bind} positional argument no.2 must be either of type "
                f"{str} for adding an event by that name, "
                f"of type {EndpointBuilder} for adding an endpoint, "
                f"of type {WebSocketEndpoint} for adding a websocket endpoint, "
                f"of type {Middleware} for adding a middleware, "
                f"or of type {ExceptionHandler} for adding an exception handler, "
                f"got: {type(args[0])}"
            )

def add_all(app: App, bound: Iterable[Bound]) -> list[Added]:

    return [add(app, b) for b in bound]

_B = TypeVar("_B", Bound, Built)

def clone(bound: _B) -> _B:

    return bound.clone()

def clone_all(bound: Iterable[_B]) -> list[_B]:

    return list(map(clone, bound))

class Builder(metaclass=ABCMeta):

    websocket = build_websocket_endpoint
    exception_handler = build_exception_handler
    endpoint = build_endpoint
    middleware = build_middleware
    event = build_event

class AutoFasAPI:

    def __init__(
            self,
            app: App = None,
            bound: Iterable[Bound] = None,
            added: Iterable[Added] = None,
            added_bound: Iterable[Bound] = None
    ) -> None:

        if added_bound is None:
            added_bound = []

        if bound is None:
            bound = []

        if added is None:
            added = []

        self.app = app
        self.bound = bound
        self.added_bound = added_bound
        self.added = added

        self.build = Builder

    def clone(self) -> Self:

        return AutoFasAPI(
            app=self.app,
            bound=clone_all(self.bound),
            added=self.added.copy()
        )

    def bind(self, c, built: Built) -> Bound:

        bound = bind(c, built)

        self.bound.append(bound)

        return bound

    def bind_all(self, data: Iterable[tuple[Callable, Built]]) -> list[Bound]:

        bound = bind_all(data)

        self.bound.extend(bound)

        return bound

    @overload
    def add(self, bound: Bound) -> Added:

        pass

    @overload
    def add(self, app: App, bound: Bound) -> Added:

        pass

    def add(self, app: App = None, bound: Bound = None) -> Added:

        if (app, self.app) == (None, None):
            raise ValueError("App is not given nor defined.")

        if bound is None:
            raise TypeError("bound must be given.")

        self.app = app

        added = add(app, bound)

        self.added.append(added)

        return added

    def add_all(self, app: App = None) -> list[Added]:

        added = []

        for bound in self.bound.copy():
            a = self.add(app, bound)

            added.append(a)
            self.added.append(a)
            self.bound.remove(bound)
            self.added_bound.append(bound)

        return added

    @overload
    def push(self, data: tuple[Callable, Built]) -> Added:

        pass

    @overload
    def push(self, app: App, data: tuple[Callable, Built]) -> Added:

        pass

    def push(
            self,
            app: App = None,
            data: tuple[Callable, Built] = None
    ) -> Added:

        if (app, self.app) == (None, None):
            raise ValueError("App is not given nor defined.")

        if data is None:
            raise TypeError("bound must be given.")

        return self.add(app, self.bind(*data))

    @overload
    def push_all(
            self,
            data: Iterable[tuple[Callable, Built]]
    ) -> list[Added]:

        pass

    @overload
    def push_all(
            self,
            app: App,
            data: Iterable[tuple[Callable, Built]]
    ) -> list[Added]:

        pass

    def push_all(
            self,
            app: App = None,
            data: Iterable[tuple[Callable, Built]] = None
    ) -> list[Added]:

        return [self.add(app, self.bind(c, built)) for c, built in data]
