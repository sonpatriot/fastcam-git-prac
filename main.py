from fastapi import FastAPI
from pydantic import BaseModel #데이터를 전송할 때 규약을 정의해주는 라이브러리
from typing import Optional #반드시 필요한 것은 아니라는 라이브러리

app = FastAPI()
"""
CRUD
Create, Read, Update, Delete
@app.post : Create
@app.get : Read
@app.put : Update
@app.delete : Delete
"""
######Path Parameter
# @app.get("/") #get-method로 접근
# def read_root():
# return {"Hello": "World"}

items = {
    0 : {"name":"bread", "price":1000},
    1 : {"name":"water", "price":500},
    2 : {"name":"lamyun", "price":1200}
}

class Item(BaseModel):
   name : str
   price : int 

@app.get("/items/{item_id}") #items라는 변수명에 item_id키에 접근
#http://127.0.0.1:8000/items/1 이렇게 호출함
def read_item(item_id: int): #자료형에 대한 hint
    item = items[item_id]
    return item

@app.post('/items/{item_id}')
def create_item(item_id:int, item: Item):
   if item_id in items:
      return {"error":"There is already existing key."}
   items[item_id] = item.dict()
   return {"success":"ok"}

class ItemForUpdate(BaseModel):
   name : Optional[str]
   price : Optional[int]

@app.put("/items/{item_id}")
def update_item(item_id:int, item: ItemForUpdate):
   if item_id not in items:
      return{"error": f"There is no item id : {item_id}"}
   if item.name:
      item[item_id]['name'] = item.name
   if item.price:
      item[item_id]['price'] = item.price
   return {"success":"ok"}