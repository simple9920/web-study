from pydantic import BaseModel, Field, EmailStr

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: int = Field(..., gt=0)
    description: str | None = Field(None, max_length=200)

class ItemUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: int = Field(..., gt=0)
    description: str | None = Field(None, max_length=200)

class ItemResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=50)
    price: int = Field(..., gt=0)
    description: str | None = Field(None, max_length=200)
    user_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):#リクエストボディの型定義
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=72)

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class Item(BaseModel):
    id: int
    name: str
    price: int
    description: str
    user_id: int

    class Config:
        from_attributes = True
    