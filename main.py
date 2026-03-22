from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

#データモデル
class Item(BaseModel):
    id: int
    name: str
    price: int
    description: str | None = None

#仮想DB
items = []

#Create
@app.post("/items/")
def create_item(item: Item):
    items.append(item)
    return item

#Read
@app.get("/items/{item_id}")
def get_items(item_id: int):
    for item in items:
        if item.id == item_id:
            return items
    raise HTTPException(status_code=404, detail="Item not found")

#update
@app.put("/items/{item_id}")
def update_item(item_id: int, new_item: Item):
                for index, item in enumerate(items):
                      if item.id == item_id:
                            items[index] = new_item
                            return new_item
                raise HTTPException(status_code=404, detail="Item not found")

#Delete
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
      for index, item in enumerate(items):
            if item.id == item_id:
                  items.pop(index)
                  return {"message": "deleted"}
      raise HTTPException(status_code=404, detail="Item not found")