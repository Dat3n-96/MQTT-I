# mqtt_hmac

Lightweight library that extends MQTT-style messages with an HMAC integrity
signature. The package implements a small, pluggable HMAC abstraction and a
wire-format encoder/decoder so messages can be signed and verified with a
configurable hash algorithm (default: SHA-256).

**Wire Format**
- **Fixed Header**: 1 byte
- **Topic Length**: 2 bytes (big-endian unsigned)
- **Topic**: UTF-8 encoded bytes (length above)
- **HMAC Length**: 2 bytes (big-endian unsigned)
- **HMAC Signature**: raw bytes (length above)
- **Payload**: remaining bytes

**Design Rationale**
- **Integrity scope**: the HMAC is computed over `topic_bytes + payload` by
	default. That choice keeps the signed material explicit and small; if you
	need to cover additional MQTT fields you can compute the signature over a
	different concatenation before calling `encode_packet`.
- **Pluggable hash**: the HMAC implementation is abstracted behind a small
	`HmacSigner` protocol. The default `HmacSha` uses `hashlib` and accepts a
	`hash_name` (e.g. `sha256`, `sha512`) so switching algorithms is easy.

**Installation**
- **Local dev**: this repository uses a `src/` layout. In development, add the
	`src` directory to `PYTHONPATH` or use a local editable install:

```powershell
python -m pip install -e .
```

**Environment setup (recommended)**

Create an isolated virtual environment and install the project's requirements:

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

macOS / Linux (bash):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If you prefer `pytest` locally, the `requirements.txt` file already includes
`pytest` so tests can be run with `pytest` once the virtual environment is
activated.

**Quick Example**
- **Encoding a packet**:

```python
from mqtt_hmac import MqttHmacPacket, encode_packet, decode_packet, HmacSha

key = b"secret123"
pkt = MqttHmacPacket(fixed_header=0x30, topic="sensors/1", signature=None, payload=b"hello")
raw = encode_packet(pkt, key=key, signer=HmacSha())
```

- **Decoding and verifying**:

```python
decoded = decode_packet(raw, key=key, signer=HmacSha())
assert decoded.topic == "sensors/1"
assert decoded.payload == b"hello"
```

**API Reference (short)**
- **`MqttHmacPacket`**: dataclass with `fixed_header: int`, `topic: str`,
	`signature: Optional[bytes]`, `payload: bytes`.
- **`encode_packet(packet, key, signer=None)`**: returns bytes in wire format.
	If `packet.signature` is `None`, `key` is required to compute the signature.
- **`decode_packet(data, key, signer=None)`**: parses bytes into
	`MqttHmacPacket`. If `key` is provided, the HMAC is verified and
	`HmacVerificationError` is raised on mismatch.
- **`HmacSha(hash_name='sha256')`**: default HMAC signer using `hashlib`.

**How to change the hash algorithm**
- Option A — use a different built-in hash:

```python
from mqtt_hmac import HmacSha
signer = HmacSha(hash_name='sha512')
raw = encode_packet(pkt, key=key, signer=signer)
```

- Option B — implement your own signer by matching the `HmacSigner` protocol:

```python
class MySigner:
		def sign(self, key: bytes, data: bytes) -> bytes: ...
		def verify(self, key: bytes, data: bytes, sig: bytes) -> bool: ...

raw = encode_packet(pkt, key=key, signer=MySigner())
```

**Running tests (without pytest)**
- Quick runner included for environments without `pytest`:

```powershell
python tests/run_tests.py
```

**Security notes**
- Use a strong secret key and manage it securely (do not hard-code secrets in
	source). Prefer dedicated secret management or environment variables.
- HMAC protects integrity and authenticity when the key is secret; it does
	not provide confidentiality — use TLS/DTLS if you need encryption.

**Contributing**
- Please open an issue describing changes before sending larger patches.
- Add unit tests for new functionality and follow the existing `src/` layout.

# mqtt-hmac

Modified MQTT framing that adds an HMAC signature for integrity.

Structure used:

- [Fixed Header] (1 byte)
- [Topic Length] (2 bytes, big-endian)
- [Topic Name] (utf-8)
- [HMAC Signature] (variable, from hash digest size)
- [Payload] (bytes)

Design goals
- SOLID principles: small single-responsibility modules and dependency injection for HMAC algorithm
- HMAC uses SHA-256 by default but the hashing algorithm is pluggable

Quick usage example (Python):

```py
from mqtt_hmac.hmac_strategy import HashlibHMACStrategy
from mqtt_hmac.framing import Framer
import hashlib

key = b'secret'
strategy = HashlibHMACStrategy(hashlib.sha256)
framer = Framer(strategy, key)

frame = framer.create_frame(0x30, 'sensors/temp', b'23.5')
parsed = framer.parse_frame(frame)
assert parsed['valid']
```

See `tests/` for more examples.
