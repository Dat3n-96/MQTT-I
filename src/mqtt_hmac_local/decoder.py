import struct
from .packet import MqttHmacPacket
from .crypto import HmacSha
from .exceptions import InvalidPacketError, HmacVerificationError


def _read_u16_be(b: bytes, offset: int) -> tuple[int, int]:
    if offset + 2 > len(b):
        raise InvalidPacketError("unexpected end of packet while reading length")
    return struct.unpack_from(
        ">H", b, offset
    )[0], offset + 2


def decode_packet(data: bytes, key: bytes | None, signer=None) -> MqttHmacPacket:
    if signer is None:
        signer = HmacSha()

    if len(data) < 1:
        raise InvalidPacketError("packet too short: no fixed header")

    offset = 0
    fixed_header = data[0]
    offset = 1

    topic_len, offset = _read_u16_be(data, offset)
    if offset + topic_len > len(data):
        raise InvalidPacketError("packet too short for topic bytes")
    topic_bytes = data[offset : offset + topic_len]
    offset += topic_len
    topic = topic_bytes.decode("utf-8")

    sig_len, offset = _read_u16_be(data, offset)
    if offset + sig_len > len(data):
        raise InvalidPacketError("packet too short for signature bytes")
    signature = data[offset : offset + sig_len]
    offset += sig_len

    payload = data[offset:]

    if key is not None:
        if not signer.verify(key, topic_bytes + payload, signature):
            raise HmacVerificationError("HMAC verification failed")

    return MqttHmacPacket(fixed_header=fixed_header, topic=topic, signature=signature, payload=payload)
