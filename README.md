# auto-fastapi

> A pythonic functional way to construct FastAPI applications be declaring endpoints in separation of their functional definition, enabeling to separate, replicate, and reuse functions in different APIs at the same time, and also run multiple of them.

## Installation
```
pip install autl-fastapi
```

## example

```python
from fastapi import FastAPI

from auto_fastapi import Method, AutoFastAPI, Builder, Server, Config


def startup() -> None:
    print("startup")


def login(username: str, password: str) -> dict[str, str | dict[str, str]]:
    return {
        "response": "success",
        "request": dict(username=username, password=password)
    }


app = FastAPI()

auto = AutoFastAPI(app)
auto.push((startup, Builder.event("startup")))
auto.push((login, Builder.endpoint("/login", [Method.GET])))

server = Server(Config(app, host="127.0.0.1", port=5555))
server.run()
```

to stop the server
```python
server.exit()
```

to run again
```python
server.run()
```