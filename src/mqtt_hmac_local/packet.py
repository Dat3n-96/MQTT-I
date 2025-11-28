from dataclasses import dataclass


@dataclass
class MqttHmacPacket:
    fixed_header: int
    topic: str
    signature: bytes | None
    payload: bytes
