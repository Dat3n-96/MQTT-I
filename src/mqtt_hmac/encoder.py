"""Encoder for the modified MQTT/HMAC packet format."""
from __future__ import annotations

from typing import Optional
import struct

from .packet import MqttHmacPacket
from .crypto import HmacSigner, HmacSha


def _u16_be(x: int) -> bytes:
    return struct.pack(
        ">H", x
    )  # big-endian unsigned short (2 bytes) - topic and signature lengths


def encode_packet(packet: MqttHmacPacket, key: Optional[bytes], signer: Optional[HmacSigner] = None) -> bytes:
    """Encode a `MqttHmacPacket` to wire format.

    If `key` is provided and `packet.signature` is None, the function will compute
    the HMAC using `signer` (defaults to SHA-256).
    """
    if signer is None:
        signer = HmacSha()

    if not (0 <= packet.fixed_header <= 0xFF):
        raise ValueError("fixed_header must be a single byte value")

    topic_bytes = packet.topic.encode("utf-8")
    payload = packet.payload or b""

    # compute signature if needed
    signature = packet.signature
    if signature is None:
        if key is None:
            raise ValueError("key is required to compute signature when packet.signature is None")
        to_sign = topic_bytes + payload
        signature = signer.sign(key, to_sign)

    out = bytearray()
    out.append(packet.fixed_header & 0xFF)
    out += _u16_be(len(topic_bytes))
    out += topic_bytes
    out += _u16_be(len(signature))
    out += signature
    out += payload
    return bytes(out)
