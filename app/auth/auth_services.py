from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from starlette import status
from app.app_models import User
from app.auth.auth_models import Token
from settings import SECRET_KEY
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
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


async def authenticate_user(current_user: User = Depends(get_current_user)):
    return current_user


async def create_access_token(data: dict, expires_delta=timedelta(minutes=15)):
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
