# Design Notes — mqtt_hmac

This document explains the packet layout, signing scope, and extensibility
decisions made for the `mqtt_hmac` project.

**Wire format**
- `Fixed Header` (1 byte): preserved for compatibility with MQTT-like framing.
- `Topic Length` (2 bytes, BE): length of the topic in bytes.
- `Topic` (variable): UTF-8 encoded topic string.
- `HMAC Length` (2 bytes, BE): length of the signature in bytes.
- `HMAC Signature` (variable): raw HMAC bytes.
- `Payload` (remaining bytes): the message body.

**Signed material**
- Currently the HMAC is computed over `topic_bytes + payload`.
- Rationale: keeps the scope minimal and deterministic. It allows receivers to
  verify that the payload came for a specific topic without ambiguity.

**Extensibility / Hash algorithm**
- The package exposes a `HmacSigner` protocol (a tiny interface) and a
  built-in `HmacSha` implementation backed by `hashlib`.
- To change hash algorithm, construct `HmacSha(hash_name='sha512')`, or
  implement a new signer and pass it to `encode_packet`/`decode_packet`.

**Encoder/Decoder responsibilities**
- `encoder` composes the bytes according to the wire format and computes the
  signature if omitted in the `MqttHmacPacket`.
- `decoder` parses fields, verifies the signature when a `key` is provided,
  and returns the `MqttHmacPacket` model.

**Security considerations**
- HMAC assumes a secret symmetric key. Keep keys confidential and rotate
  them as needed.
- The design does not provide replay protection or anti-replay counters. If
  you need them, include timestamp/nonce in the payload and verify freshness.

**Potential future work**
- Add optional fields for signing additional MQTT headers (QoS, packet id).
- Add a negotiation layer for signer parameters (hash algorithm + key id).
- Integrate with TLS or other transport-level security for confidentiality.
