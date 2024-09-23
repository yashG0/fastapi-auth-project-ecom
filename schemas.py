from pydantic import BaseModel, Field, EmailStr

class ProductSchema(BaseModel):
    name:str = Field(min_length=3, max_length=32, title="Product Name", description="Enter the name of product.")
    description:str = Field(min_length=8, max_length=255, title="Product Description", description="Detailed information about the product")
    price:float = Field(gt=0, title="Price", description="Price of the product, must be greater than zero")
    stock:int = Field(default=0, title="Stock", description="Available stock for the product")
    category:str|None = Field(default=None, title="Category", description="Optional category of the product")


class UserSchema(BaseModel):
    username:str = Field(min_length=3, max_length=22, title="Username", description="User's unique username")
    email:EmailStr = Field(title="Email", description="Valid email address of the user")
    password:str = Field(min_length=6, max_length=72,title="Password", description="Password must be between 6 and 72 characters long")


class UserIn(BaseModel):
    username:str = Field(min_length=3, max_length=22, title="Username", description="User's unique username")
    password:str = Field(min_length=6, max_length=72,title="Password", description="Password must be between 6 and 72 characters long")


class UserOut(BaseModel):
    userId:int
    username:str

class PasswordSchema(BaseModel):
    password:str = Field(min_length=6, max_length=72,title="Password", description="Password must be between 6 and 72 characters long")
    newPassword:str = Field(min_length=6, max_length=72,title="Password", description="Password must be between 6 and 72 characters long")