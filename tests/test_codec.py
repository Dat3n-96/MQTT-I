import os
import sys

# Ensure `src` is on sys.path so tests can import the package in this workspace layout.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from mqtt_hmac_local import MqttHmacPacket, encode_packet, decode_packet, HmacSha
from mqtt_hmac_local.exceptions import HmacVerificationError


def test_encode_decode_roundtrip():
    key = b"mytestkey"
    pkt = MqttHmacPacket(fixed_header=0x30, topic="test/topic", signature=None, payload=b"payload-data")
    raw = encode_packet(pkt, key=key, signer=HmacSha())
    decoded = decode_packet(raw, key=key, signer=HmacSha())
    assert decoded.fixed_header == pkt.fixed_header
    assert decoded.topic == pkt.topic
    assert decoded.payload == pkt.payload


def test_signature_mismatch():
    key = b"key1"
    pkt = MqttHmacPacket(fixed_header=0x30, topic="t", signature=None, payload=b"p")
    raw = encode_packet(pkt, key=key, signer=HmacSha())
    # tamper with payload
    tampered = raw[:-1] + b"x"
    try:
        decode_packet(tampered, key=key, signer=HmacSha())
    except HmacVerificationError:
        return
    raise AssertionError("tampered packet should have caused HMAC verification error")
