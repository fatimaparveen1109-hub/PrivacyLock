import hashlib
import secrets

# Demo-only token helper. Use a maintained auth library, password hashing and signed
# sessions/JWT with expiry before deployment.
def make_token():
    return secrets.token_urlsafe(24)

def demo_password_hash(password: str) -> str:
    # Not suitable for production password storage.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
