"""Packet model for the modified MQTT with HMAC signature.

Layout used by encoder/decoder:

[Fixed Header: 1 byte]
[Topic Length: 2 bytes big-endian unsigned]
[Topic: variable utf-8 bytes]
[HMAC Length: 2 bytes big-endian unsigned]
[HMAC Signature: variable bytes]
[Payload: rest of bytes]

Notes:
- The HMAC is computed over `topic_bytes + payload` by default.
  This is a deliberate, simple choice and can be changed in
  `encoder.py`/`decoder.py` if needed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class MqttHmacPacket:
    fixed_header: int
    topic: str
    signature: Optional[bytes]
    payload: bytes

    def __repr__(self) -> str:  # pragma: no cover - convenience only
        sig = f"{len(self.signature) if self.signature else 0} bytes"
        return (
            f"MqttHmacPacket(fixed_header={self.fixed_header}, topic={self.topic!r}, "
            f"signature={sig}, payload={len(self.payload)} bytes)"
        )
