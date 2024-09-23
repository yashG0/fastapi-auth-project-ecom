from fastapi import APIRouter, Depends, HTTPException, Request,  status
from sqlalchemy.orm import Session


from ..utils import createHashPasswd, validateHashPasswd
from ..db import getDb
from ..models import Users
from ..routers.authRoute import getUser
from ..schemas import PasswordSchema, UserOut
from .authRoute import templates

userRoutes = APIRouter(prefix="/api/user", tags=["My User Routes"])

# PAGES ->
@userRoutes.get("/profile-page")
async def updatePasswordPage(req:Request):
    return templates.TemplateResponse(name="profile.html", context={"request":req})

# ENDPOINTs ->
@userRoutes.get("/userInfo", status_code=status.HTTP_200_OK)
async def getUserInfo(db:Session = Depends(getDb), userInfo:UserOut = Depends(getUser)):
    if not userInfo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized!")

    currentUser = db.query(Users).filter(Users.id == userInfo.userId).first()

    if not currentUser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return currentUser


@userRoutes.put("/updatePassword", status_code=status.HTTP_204_NO_CONTENT)
async def updatePassword(userPasswd:PasswordSchema,db:Session = Depends(getDb), userInfo:UserOut = Depends(getUser)):
    if not userInfo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized!")

    currentUser = db.query(Users).filter(Users.id == userInfo.userId).first()

    if not currentUser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not isinstance(currentUser.password, str):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User password is not set")

    if not validateHashPasswd(userPasswd.password, str(currentUser.password)):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Password! please enter correct Password")

    try:
        currentUser.password = createHashPasswd(userPasswd.newPassword) # type: ignore
        db.add(currentUser)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error occurred while updating password: {e}")
