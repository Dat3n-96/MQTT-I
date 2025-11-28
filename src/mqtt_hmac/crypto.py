"""HMAC abstraction and default implementations.

This module defines a small HMAC signer interface (`HmacSigner`) and a
default `HmacSha` implementation that uses Python's `hmac` and `hashlib`.

The design keeps the hash algorithm pluggable: to change the hash, provide
another `HmacSigner` implementation or construct `HmacSha` with a different
`hash_name` (e.g., 'sha1', 'sha512').
"""
from __future__ import annotations

import hmac
import hashlib
from typing import Protocol


class HmacSigner(Protocol):
    """Protocol for HMAC signer implementations."""

    def sign(self, key: bytes, data: bytes) -> bytes:
        """Return the HMAC signature for `data` using `key`."""

    def verify(self, key: bytes, data: bytes, signature: bytes) -> bool:
        """Return True if `signature` is valid for `data` and `key`."""


class HmacSha:
    """HMAC implementation using hashlib (SHA family).

    Parameters:
    - hash_name: name accepted by `hashlib.new`, default 'sha256'.
    """

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
