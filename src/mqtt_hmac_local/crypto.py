"""HMAC abstraction and default implementations for local package."""
from __future__ import annotations

import hmac
import hashlib
from typing import Protocol


class HmacSigner(Protocol):
    def sign(self, key: bytes, data: bytes) -> bytes:
        pass

    def verify(self, key: bytes, data: bytes, signature: bytes) -> bool:
        pass


class HmacSha:
    def __init__(self, hash_name: str = "sha256") -> None:
        self.hash_name = hash_name

    @property
    def digest_size(self) -> int:
        return hashlib.new(self.hash_name).digest_size

    def sign(self, key: bytes, data: bytes) -> bytes:
        return hmac.new(key, data, digestmod=self.hash_name).digest()

    def verify(self, key: bytes, data: bytes, signature: bytes) -> bool:
        expected = self.sign(key, data)
        return hmac.compare_digest(expected, signature)
