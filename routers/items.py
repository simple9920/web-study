from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import ItemCreate, ItemUpdate, ItemResponse
import crud, schemas
from dependencies import get_current_user
from models import User

router = APIRouter(
    prefix="/items",
    tags=["items"]
)
#全ユーザー共通データ
@router.post("/", response_model=ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return crud.create_item(db, item, current_user.id)

def get_my_items(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return crud.get_items_by_user(db, current_user.id)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = crud.get_item(db, item_id, current_user.id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int,
    new_item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    item = crud.update_item(db, item_id, new_item,current_user.id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item

@router.delete("/{item_id}")
def delete_item(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = crud.delete_item(db, item_id, current_user.id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted"}

