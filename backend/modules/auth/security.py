import hashlib
import hmac
import os


def hash_password(password: str) -> str:
    """Hash a plaintext password using PBKDF2 with SHA-256 and a random salt."""
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plaintext password against a stored PBKDF2 hash string."""
    if not stored_hash or "$" not in stored_hash:
        return False
    try:
        salt, digest = stored_hash.split("$", 1)
    except ValueError:
        return False

    check = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()
    return hmac.compare_digest(check, digest)
