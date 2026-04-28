import jwt

from datetime import datetime, timezone

from typing import Optional

 

# VULNERABILITY #2: weak hardcoded JWT secret.

# In a real system this would be in an env var with high entropy.

# This makes brute-force / known-secret attacks trivial.

JWT_SECRET = "secret123"

JWT_ALGORITHM = "HS256"

 

# VULNERABILITY #3: token has no expiry claim.

# Once issued, valid forever — no way to revoke without rotating the secret.

def create_token(username: str, role: str) -> str:

    payload = {

        "sub": username,

        "role": role,

        "iat": int(datetime.now(timezone.utc).timestamp()),

        # NOTE: deliberately no 'exp' claim

    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> Optional[dict]:

    try:

        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

    except jwt.PyJWTError:

        return None