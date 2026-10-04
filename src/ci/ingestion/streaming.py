import json
from typing import Any, Callable

class EventConsumer:
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self._is_running = False

    def start(self, callback: Callable[[dict[str, Any]], None]) -> None:
        self._is_running = True

    def stop(self) -> None:
        self._is_running = False

    def process_message(
        self, raw_message: str, callback: Callable[[dict[str, Any]], None]
    ) -> None:
        try:
            data = json.loads(raw_message)
            callback(data)
        except json.JSONDecodeError:
            pass

class EventProducer:
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

    def send(self, data: dict[str, Any]) -> bool:
        try:
            json.dumps(data)
            return True
        except TypeError:
            return False
