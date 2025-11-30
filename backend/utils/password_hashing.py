import hashlib

def hash_password(password: str) -> str:
    """Simple SHA-256 hash"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a plain-text password against a stored password hash.
    """
    return hash_password(password) == password_hash
