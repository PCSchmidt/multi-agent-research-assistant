"""Encryption utilities for API key storage."""

import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

from app.config import settings


def _get_encryption_key() -> bytes:
    """
    Derive encryption key from settings.

    Uses PBKDF2 to derive a Fernet-compatible key from the encryption password.

    Returns:
        32-byte encryption key
    """
    # Use a fixed salt (in production, this should be stored separately)
    # For now, use a hash of the Supabase URL as salt (deterministic but unique per project)
    salt = settings.supabase_url.encode()[:16].ljust(16, b"0")

    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    # Derive key from the encryption password (service role key)
    key = kdf.derive(settings.supabase_service_role_key.encode())
    return base64.urlsafe_b64encode(key)


def encrypt_api_key(api_key: str) -> str:
    """
    Encrypt an API key for storage.

    Args:
        api_key: Plain text API key

    Returns:
        Base64-encoded encrypted key
    """
    fernet = Fernet(_get_encryption_key())
    encrypted = fernet.encrypt(api_key.encode())
    return base64.b64encode(encrypted).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """
    Decrypt an API key from storage.

    Args:
        encrypted_key: Base64-encoded encrypted key

    Returns:
        Plain text API key

    Raises:
        InvalidToken: If decryption fails
    """
    fernet = Fernet(_get_encryption_key())
    encrypted_bytes = base64.b64decode(encrypted_key.encode())
    decrypted = fernet.decrypt(encrypted_bytes)
    return decrypted.decode()
