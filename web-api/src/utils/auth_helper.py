from datetime import datetime, timezone, timedelta
import functools
from fastapi import Request, Response
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.data_access.data_access import SessionLocal
from src.data_models.user_data_model import UserDataModel


crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "caf575c0dfe3a146e407f21f58b01f416e6315172121e4c5bdac47dd399e744f"
ALGORITHM = "HS256"

MAIL_SERVICE_API_KEYS = ['748ee205c20364e9da1efd637a35a217a7699628a688cba7956d76ca0690b00b', '81f81296976b6010fff75bd1196edea6ad05a6fe9ee995372430ddcb3155e681']

def get_password_hash(password: str):
    return crypto_context.hash(password)


def verify_passwords(hashed_password, user_password):
    return crypto_context.verify(hashed_password, user_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    claims = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    claims.update({"exp": expire})
    token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)

    return token


def authorize(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request | None = kwargs.get("request")
        if request is None:
            return Response(status_code=403)

        authorization_header = request.headers.get("Authorization")
        if authorization_header is not None:
            if 'Bearer' in authorization_header:
                token = authorization_header.replace("Bearer ", "")
                try:
                    claims = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
                    subject = claims.get("sub")
                except JWTError:
                    return Response(status_code=403)

                with SessionLocal() as session:
                    user = (
                        session.query(UserDataModel)
                        .where(UserDataModel.email == subject)
                        .first()
                    )

                    if user is None:
                        return Response(status_code=403)
            else:
                api_key = next((key for key in MAIL_SERVICE_API_KEYS if key == authorization_header), None)
                if api_key is None:
                    return Response(status_code=403)

            result = await func(*args, **kwargs)

        return result

    return wrapper
