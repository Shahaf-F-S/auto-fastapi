# server.py

import asyncio
import socket
import time

from uvicorn import Server as BaseServer, Config

__all__ = [
    "Server",
    "Config"
]

class Server:

    def __init__(self, config: Config) -> None:

        self._running = False

        self.config = config

        self.server = BaseServer(self.config)

    @property
    def running(self) -> bool:

        return self._running

    def run(self, sockets: list[socket.socket] = None) -> None:

        self.config.setup_event_loop()

        self._running = True

        asyncio.run(self.server.serve(sockets=sockets))

        self._running = False

    def exit(self) -> None:

        self.server.should_exit = True

        while self.running:
            time.sleep(0.0001)
