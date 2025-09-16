"""Lightweight TOTP helpers compatible with Google Authenticator."""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import struct
import time
from typing import Optional


def random_base32_secret(length: int = 32) -> str:
    """Generate a base32 encoded secret compatible with Google Authenticator."""
    # Base32 requires 5 bits per character, therefore we request enough random
    # bytes and then strip the padding.
    random_bytes = os.urandom(length)
    encoded = base64.b32encode(random_bytes).decode('utf-8')
    return encoded.strip('=')[:length]


def _int_to_bytes(value: int) -> bytes:
    return struct.pack('>Q', value)


def totp_token(secret: str, *, digits: int = 6, interval: int = 30, timestamp: Optional[float] = None,
               digest: str = 'sha1') -> str:
    """Generate the current TOTP token for the provided secret."""
    if timestamp is None:
        timestamp = time.time()

    counter = int(timestamp // interval)
    key = base64.b32decode(secret.upper() + '=' * (-len(secret) % 8))
    hash_func = getattr(hashlib, digest)
    hm = hmac.new(key, _int_to_bytes(counter), hash_func).digest()
    offset = hm[-1] & 0x0F
    truncated = hm[offset:offset + 4]
    code_int = struct.unpack('>I', truncated)[0] & 0x7FFFFFFF
    token = code_int % (10 ** digits)
    return str(token).zfill(digits)


def verify_totp(secret: str, token: str, *, digits: int = 6, interval: int = 30, window: int = 1) -> bool:
    """Validate a token allowing the provided window (in steps)."""
    if not token or not token.isdigit():
        return False

    token = token.zfill(digits)
    current_time = time.time()
    for offset in range(-window, window + 1):
        comparison_time = current_time + (offset * interval)
        if totp_token(secret, digits=digits, interval=interval, timestamp=comparison_time) == token:
            return True
    return False


def provisioning_uri(secret: str, username: str, issuer: str) -> str:
    """Build an otpauth URI string that can be used for QR code generation."""
    from urllib.parse import quote

    label = quote(f"{issuer}:{username}")
    issuer_q = quote(issuer)
    return f"otpauth://totp/{label}?secret={secret}&issuer={issuer_q}"
