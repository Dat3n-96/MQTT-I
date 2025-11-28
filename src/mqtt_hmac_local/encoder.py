import struct
from .packet import MqttHmacPacket
from .crypto import HmacSha


def _u16_be(x: int) -> bytes:
    return struct.pack(
        ">H", x
    )


def encode_packet(packet: MqttHmacPacket, key: bytes | None, signer=None) -> bytes:
    if signer is None:
        signer = HmacSha()

    topic_bytes = packet.topic.encode("utf-8")
    payload = packet.payload or b""

    signature = packet.signature
    if signature is None:
        if key is None:
            raise ValueError("key is required to compute signature")
        signature = signer.sign(key, topic_bytes + payload)

    out = bytearray()
    out.append(packet.fixed_header & 0xFF)
    out += _u16_be(len(topic_bytes))
    out += topic_bytes
    out += _u16_be(len(signature))
    out += signature
    out += payload
    return bytes(out)
