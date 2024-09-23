from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..models import Products, Users
from ..routers.authRoute import getUser
from ..db import getDb
from ..schemas import ProductSchema, UserOut
from .authRoute import templates

productRouters = APIRouter(tags=["My Product Route"], prefix="/api/product")

# PAGEs
@productRouters.get("/add-product-page")
async def addProductPage(req:Request):
    return templates.TemplateResponse(name="addProduct.html", context={"request":req})


# ENDPOINTs
@productRouters.post("/add", status_code=status.HTTP_201_CREATED)
async def addProduct(newProduct:ProductSchema, db:Session = Depends(getDb), userInfo:UserOut = Depends(getUser)):
   
    user = db.query(Users).filter(Users.id == userInfo.userId).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does'nt Exists!")
    
    try:
        newProductObj =  Products(
            name = newProduct.name,
            description = newProduct.description,
            price = newProduct.price,
            stock = newProduct.stock,
            category = newProduct.category,
            userId = userInfo.userId
        )
        
        db.add(newProductObj)
        db.commit()
        return {"success":True,"message": "Product added successfully"}

        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occured during adding new product: {e}")