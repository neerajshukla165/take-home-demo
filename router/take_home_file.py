from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncpg
from typing import List
from db import get_pool, Item

file_router = APIRouter(
    prefix="/files"
)

 # Route to create a new item in the database
@file_router.post("/items/")
async def create_item(item: Item):
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            # Check if folder_id exists
            folder_query = "SELECT id FROM folders WHERE id = $1"
            folder_exists = await conn.fetchval(folder_query, item.folder_id)
            if not folder_exists:
                raise HTTPException(status_code=404, detail="Folder not found")
            
            # Insert item into items table
            insert_query = "INSERT INTO items (id, name, path, folder_id) VALUES ($1, $2, $3, $4)"
            await conn.execute(insert_query, item.id, item.name, item.path, item.folder_id)
            return {"message": "Item created successfully"}
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(status_code=400, detail="Item with this id already exists")


# Route to retrieve items by folder ID
@file_router.get("/folders/{folder_id}/items/", response_model=List[Item])
async def get_items_by_folder(folder_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        items_query = "SELECT id, name, path, folder_id FROM items WHERE folder_id = $1"
        rows = await conn.fetch(items_query, folder_id)
        return [dict(row) for row in rows]


 # Route to update an existing item by item ID
@file_router.put("/items/{item_id}/")
async def update_item(item_id: int, item: Item):
    pool = await get_pool()
    async with pool.acquire() as conn:
        update_query = "UPDATE items SET name = $1, path = $2, folder_id = $3 WHERE id = $4"
        await conn.execute(update_query, item.name, item.path, item.folder_id, item_id)
        return {"message": "Item updated successfully"}


# Route to delete an item by item ID
@file_router.delete("/items/{item_id}/")
async def delete_item(item_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        delete_query = "DELETE FROM items WHERE id = $1"
        await conn.execute(delete_query, item_id)
        return {"message": "Item deleted successfully"}


# Route to retrieve all items
@file_router.get("/items/", response_model=List[Item])
async def get_all_items():
    pool = await get_pool()
    async with pool.acquire() as conn:
        items_query = "SELECT id, name, path, folder_id FROM items"
        rows = await conn.fetch(items_query)
        return [dict(row) for row in rows]