from passlib.context import CryptContext
from jose import JWTError, jwt


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "OjEnmUJCND56hgnLuEpkuU7tT4pL6s7fXAGAgZS1T8s="
ALGORITHM = "HS256"

def createHashPasswd(passwd:str) -> str:
    return pwdContext.hash(passwd)


def validateHashPasswd(passwd:str, hashPasswd:str) -> bool:
    return pwdContext.verify(passwd, hashPasswd)


def createJwtToken(username:str) -> str:
    payload = {
        "sub":username
    }
    token = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def validateJwtToken(token:str) -> dict[str,str]:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError as e:
        raise JWTError(f"JWT Error: Could not validate token: {str(e)}")
