from datetime import datetime, timedelta, timezone
from jose import jwe
from dotenv import load_dotenv
import os
import base64
import json
load_dotenv()

header = {
    "alg": "dir",
    "enc": "A256CBC-HS512"
}


JWE_SECRET_KEY = os.getenv("JWE_SECRET_KEY")
if not JWE_SECRET_KEY:
    raise ValueError("The token secret key is not in os")

try:
    JWE_SECRET_KEY = base64.urlsafe_b64decode(JWE_SECRET_KEY)
    if len(JWE_SECRET_KEY) != 64:
        raise ValueError(f"JWE_SECRET_KEY must be 64 bytes. Got {len(JWE_SECRET_KEY)} bytes.")
except Exception as e:
    raise ValueError(f"Failed to decode JWE_SECRET_KEY") from e

def create_access_token(data:dict, expires_minutes:int=1440) -> str:
    payload = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_minutes)
    payload["exp"] = int(expire.timestamp())
    return jwe.serialize_compact(header,json.dumps(payload).encode(), JWE_SECRET_KEY)

def create_refresh_token(data: dict, expires_days: int = 7) -> str:
    payload = data.copy()
    expire = datetime.now() + timedelta(days=expires_days)
    payload["exp"] = int(expire.timestamp())
    return jwe.serialize_compact(header, json.dumps(payload).encode(), JWE_SECRET_KEY)