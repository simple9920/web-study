from sqlalchemy.orm import Session
from models import Item as ItemModel
from models import User
from auth import hash_password, verify_password

import models
import schemas


#create
def create_item(db: Session, item, user_id: int):
    db_item = ItemModel(
        name=item.name,
        price=item.price,
        description=item.description,
        user_id=user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#read
def get_item(db: Session, item_id: int, user_id: int):
    return db.query(ItemModel).filter(
        ItemModel.id == item_id,
        ItemModel.user_id == user_id
    ).first()



#update
def update_item(db: Session, item_id: int, new_item, user_id: int):
    item = db.query(ItemModel).filter(
        ItemModel.id == item_id,
        ItemModel.user_id == user_id
    ).first()

    if item is None:
        return None
    
    item.name = new_item.name
    item.price = new_item.price
    item.description = new_item.description
    
    db.commit()
    db.refresh(item)

    return item

#delete
def delete_item(db: Session, item_id: int, user_id: int):
    item = db.query(ItemModel).filter(
        ItemModel.id == item_id,
        ItemModel.user_id == user_id
    ).first()

    if item is None:
        return None
    
    db.delete(item)
    db.commit()

    return item

#User
def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        return None
    
    hashed_password = hash_password(user.password)

    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

#email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

#user_id
def get_items_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(ItemModel)
        .filter(ItemModel.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )