from sqlalchemy import Column, Integer, String, ForeignKey
from database import engine
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel
from pydantic import Field

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class User(Base):
    __tablename__ = "users"#DBにusersテーブルを作る
    
#各カラムの型を定義
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)