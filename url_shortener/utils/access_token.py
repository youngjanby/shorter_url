from datetime import datetime, timedelta, timezone

import jwt


SECRET_KEY = "super_secret_key_change_me_in_production"
ALGORITHM = "HS256"

def generator_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    payload = {
        "user_id": user_id,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)