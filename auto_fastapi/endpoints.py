# endpoints.py

from enum import Enum
from dataclasses import dataclass
from typing import Sequence, Callable, TypeVar, ParamSpec, Iterable

from fastapi import Response, Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.datastructures import Default
from fastapi.utils import generate_unique_id
from fastapi.routing import APIRoute, BaseRoute

__all__ = [
    "BaseEndpoint",
    "Endpoint",
    "EndpointBuilder",
    "endpoint_builder",
    "Method",
    "METHODS",
    "build_endpoints"
]

IncEx = set[int] | set[str] | dict[int, ...] | dict[str, ...]

_I = ParamSpec("_I")
_O = TypeVar("_O")

class Method(Enum):

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    UPLOAD = "UPLOAD"
    HEAD = "HEAD"
    PATCH = "PATCH"
    PUT = "PUT"

METHODS = (
    Method.GET, Method.POST, Method.DELETE, Method.UPLOAD,
    Method.HEAD, Method.PATCH, Method.PUT
)

@dataclass
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
            methods=self.methods,
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

    def endpoint(self) -> dict[str, ...]:

        data = self.data()

        data.pop("methods")

        return data

@dataclass
class Endpoint(BaseEndpoint):

    c: Callable[_I, _O] = None

@dataclass
class EndpointBuilder(BaseEndpoint):

    def build(self, c: Callable[_I, _O]) -> Endpoint:

        return Endpoint(c=c, **self.data())

def endpoint_builder(
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

def build_endpoints(
        app: FastAPI | APIRoute,
        c: Callable[_I, _O],
        builder: EndpointBuilder
) -> dict[Method, Endpoint]:

    return {
        method: getattr(app, method.value.lower())(**builder.endpoint())(c)
        for method in set(builder.methods)
        if hasattr(app, method.value.lower())
    }
