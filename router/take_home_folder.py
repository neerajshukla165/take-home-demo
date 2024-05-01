from fastapi import HTTPException, APIRouter
import asyncpg
from typing import List
from db import get_pool, Folder, MoveItem

folder_router = APIRouter(
    prefix="/folders", tags=["folder"]
)
    
# Create new folder
@folder_router.post("/create/")
async def create_folder(folder: Folder):
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            insert_query = "INSERT INTO folders (id, name) VALUES ($1, $2)"
            await conn.execute(insert_query, folder.id, folder.name)
            return {"message": "Folder created successfully"}
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(status_code=400, detail="Folder with this id already exists")
        

# Route to retrieve all folders
@folder_router.get("/fetch/", response_model=List[Folder])
async def get_all_folders():
    pool = await get_pool()
    async with pool.acquire() as conn:
        folders_query = "SELECT id, name FROM folders"
        rows = await conn.fetch(folders_query)
        return [dict(row) for row in rows]
    

# Route to update an existing folder by folder ID
@folder_router.put("/{folder_id}/")
async def update_folder(folder_id: int, folder: Folder):
    pool = await get_pool()
    async with pool.acquire() as conn:
        update_query = "UPDATE folders SET name = $1 WHERE id = $2"
        await conn.execute(update_query, folder.name, folder_id)
        return {"message": "Folder updated successfully"}
    

# Route to delete a folder by folder ID
@folder_router.delete("/{folder_id}/")
async def delete_folder(folder_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        delete_query = "DELETE FROM folders WHERE id = $1"
        await conn.execute(delete_query, folder_id)
        return {"message": "Folder deleted successfully"}


# Route to move item to other folder
@folder_router.put("/move-item/")
async def move_item(move_data: MoveItem):
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            # Check if the item exists
            item_query = "SELECT id FROM items WHERE id = $1"
            item_exists = await conn.fetchval(item_query, move_data.item_id)
            if not item_exists:
                raise HTTPException(status_code=404, detail="Item not found")

            # Check if the new folder exists
            folder_query = "SELECT id FROM folders WHERE id = $1"
            folder_exists = await conn.fetchval(folder_query, move_data.new_folder_id)
            if not folder_exists:
                raise HTTPException(status_code=404, detail="New folder not found")

            # Update the item's folder_id
            update_query = "UPDATE items SET folder_id = $1 WHERE id = $2"
            await conn.execute(update_query, move_data.new_folder_id, move_data.item_id)

            return {"message": "Item moved successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
