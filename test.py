# test.py

import time
import threading

from fastapi import FastAPI

from auto_fastapi import Method, AutoFasAPI, Builder, Server, Config

def startup() -> None:

    print("startup")

def login(username: str, password: str) -> dict[str, str | dict[str, str]]:

    return {
        "response": "success",
        "request": dict(username=username, password=password)
    }

TIMEOUT = 0

def main() -> None:

    app = FastAPI()

    AutoFasAPI().push_all(
        app,
        [
            (startup, Builder.event("startup")),
            (login, Builder.endpoint("/login", [Method.GET]))
        ]
    )

    server = Server(Config(app, host="127.0.0.1", port=5555))

    if TIMEOUT:
        threading.Thread(target=lambda: (time.sleep(TIMEOUT), server.exit())).start()

    server.run()

if __name__ == '__main__':
    main()
