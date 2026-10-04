from typing import Any

from ci.ingestion.streaming import EventConsumer, EventProducer

def handle_realtime_event(event: dict[str, Any]) -> None:
    if "Customer_ID" not in event:
        return

    producer = EventProducer(bootstrap_servers="localhost:9092", topic="processed_events")
    processed_event = {
        "Customer_ID": event["Customer_ID"],
        "Status": "Processed",
        "Original_Amount": event.get("Monetary", 0.0),
    }
    producer.send(processed_event)

def run_streaming_pipeline() -> None:
    consumer = EventConsumer(
        bootstrap_servers="localhost:9092", topic="raw_events", group_id="ci_group"
    )
    consumer.start(handle_realtime_event)
