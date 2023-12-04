from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.app_models import User
from app.auth.auth_models import Token
from settings import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.get_or_none(email=email)
    if user is None:
        raise credentials_exception
    return user


async def authenticate_user(username: str, password: str):
    user = await User.get_or_none(email=username)
    if user and user.verify_password(password):
        return user
    return None


async def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def create_token(user: User):
    expires = timedelta(minutes=30)
    access_token_expires = datetime.utcnow() + expires
    access_token = await create_access_token(
        data={"sub": user.email, "scopes": []},
        expires_delta=expires,
    )
    token = await Token.create(user=user, access_token=access_token, expires_at=access_token_expires)
    return token
