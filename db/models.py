from pydantic import BaseModel

class Folder(BaseModel):
    id: int
    name: str

class MoveItem(BaseModel):
    item_id: int
    new_folder_id: int

class Item(BaseModel):
    id: int
    name: str
    path: str
    folder_id: int

