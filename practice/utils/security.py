import bcrypt
from datetime import datetime, timedelta, UTC
from jose import jwt

def hash_password (password: str) -> str:
    "Hashing Password function"
     # convert password to bytes (bcrypt requirement)
    password_bytes = password.encode ("utf-8")

    # generate salt + hash password
    hashed = bcrypt.hashpw (password_bytes, bcrypt.gensalt())

    # convert back to string for database storage
    return hashed.decode ("utf-8")

def password_verify (plain_password: str, hashed_password: str) -> bool:
    # hash input password and then compare
    return bcrypt.checkpw (
        plain_password.encode ("utf-8"),
        hashed_password.encode ("utf-8")
    )

# upper case because are constants
SECRET_KEY = "backend_journey_fastapi_learning_secret_key_2026"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token (data: dict):
    #create a copy so we dont modify the original payload
    to_encode = data.copy()

    #calculate when the token should expire
    expire = datetime.now(UTC) + timedelta (
        minutes= ACCESS_TOKEN_EXPIRE_MINUTES
    )

    #add the expiration time to the payload copy
    to_encode.update ({"exp":expire})

    # create (sign) the JWT

    encoded_jwt = jwt.encode (
        to_encode,
        SECRET_KEY,
        algorithm= ALGORITHM
    )

    # return the JWT string
    return encoded_jwt