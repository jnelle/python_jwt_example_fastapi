import uuid
from pydantic import BaseModel
from loguru import logger
from typing import Type, TypeVar
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


Model = TypeVar("Model", bound=BaseModel)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#  https://gist.github.com/henriklindgren/f0f05034ac4b36eafdb7c877e5088f33
def load_model(t: Type[Model], o: dict) -> Model:
    populated_keys = o.keys()
    required_keys = set(t.schema()["required"])
    missing_keys = required_keys.difference(populated_keys)
    if missing_keys:
        raise ValueError(f"Required keys missing: {missing_keys}")
    all_definition_keys = t.schema()["properties"].keys()
    return t(**{k: v for k, v in o.items() if k in all_definition_keys})


def hash_password(password) -> str:
    return pwd_context.hash(password)


def check_password(hashed_password, plain_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, jwt_expire: int, jwt_secret: str, jwt_algorithm: str) -> dict:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_expire)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, jwt_secret, algorithm=jwt_algorithm)


def verify_access_token(access_token: str, jwt_secret: str, jwt_algorithm: str) -> dict:
    try:
        return jwt.decode(
            access_token, jwt_secret, algorithms=[jwt_algorithm])
    except JWTError as e:
        raise JWTError(f"Invalid token: {e}")


async def refresh_session(jwt_expire: int, jwt_secret: str, jwt_algorithm: str, decoded_token: dict, user_service: object) -> dict:
    if decoded_token["exp"] < datetime.utcnow().timestamp():
        token = decoded_token["token"]
        new_token = uuid.uuid4().hex
        await user_service.refresh_session(token, new_token)
        return create_access_token(
            data={"token": new_token},
            jwt_expire=jwt_expire,
            jwt_secret=jwt_secret,
            jwt_algorithm=jwt_algorithm
        )
