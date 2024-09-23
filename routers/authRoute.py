from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from ..utils import createHashPasswd, createJwtToken, validateHashPasswd, validateJwtToken
from ..models import Users
from ..schemas import UserOut, UserSchema
from ..db import getDb


authRoutes = APIRouter(prefix="/api/auth", tags=["My Auth Routes"])
oAuthBear = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

templates = Jinja2Templates(directory="templates")


# PAGES:
@authRoutes.get("/login-page")
async def getLoginPage(req:Request):
    return templates.TemplateResponse(name="login.html", context={"request":req})
    
    
@authRoutes.get("/signup-page")
async def getSignupPage(req:Request):
    return templates.TemplateResponse(name="signup.html", context={"request":req})
    

# ENDPOINTS:
@authRoutes.post("/signup", status_code=status.HTTP_201_CREATED)
async def createUser(user:UserSchema, db:Session = Depends(getDb)):
    try:
        isUserExist = db.query(Users).filter(Users.username == user.username).first()
        if isUserExist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Already Exists! Please Login")

        hashPassword = createHashPasswd(passwd=user.password)
        newUser = Users(
            username = user.username,
            email = user.email,
            password = hashPassword
        )
        db.add(newUser)
        db.commit()
        return {"message":"user created successfully.", "success":True}
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"ERR: {e}")


def getUser(token: str = Depends(oAuthBear), db: Session = Depends(getDb)) -> UserOut:
    try:
        payload = validateJwtToken(token)
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
        isUser = db.query(Users).filter(Users.username == username).first()
        
        return UserOut(userId=isUser.id, username=username) # type: ignore

    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid or expired")


@authRoutes.post("/login", status_code=status.HTTP_200_OK)
async def loginUser(form:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(getDb)):
    try:
        isUserExist = db.query(Users).filter(Users.username == form.username).first()

        if isUserExist is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does'nt Exists! Please Sign up")

        if not validateHashPasswd(passwd=form.password, hashPasswd=str(isUserExist.password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is invalid! please login again")

        token = createJwtToken(username=form.username)
        return {"access_token":token, "token_type":"Bearer"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Error occured: {e}")
