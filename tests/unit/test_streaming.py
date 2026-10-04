from typing import Any

from ci.ingestion.streaming import EventConsumer, EventProducer
from ci.pipelines.streaming_flow import handle_realtime_event

def test_event_producer() -> None:
    producer = EventProducer("localhost:9092", "test_topic")
    success = producer.send({"Customer_ID": 1, "Monetary": 100.0})
    assert success is True

    fail = producer.send({"Invalid": set([1, 2, 3])})
    assert fail is False

def test_event_consumer() -> None:
    consumer = EventConsumer("localhost:9092", "test_topic", "test_group")

    received_data: list[dict[str, Any]] = []

    def dummy_callback(data: dict[str, Any]) -> None:
        received_data.append(data)

    consumer.start(dummy_callback)
    assert consumer._is_running is True

    consumer.process_message('{"Customer_ID": 1}', dummy_callback)
    assert len(received_data) == 1
    assert received_data[0]["Customer_ID"] == 1

    consumer.process_message("invalid_json", dummy_callback)
    assert len(received_data) == 1

    consumer.stop()
    assert consumer._is_running is False

def test_handle_realtime_event() -> None:
    handle_realtime_event({"Customer_ID": 1, "Monetary": 50.0})
    handle_realtime_event({"Invalid": "Event"})
