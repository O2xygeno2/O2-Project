from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.database.models import Item
from sqlalchemy.future import select

router = APIRouter()

@router.post("/")
async def create_item(name: str, description: str, db: AsyncSession = Depends(get_db)):
    new_item = Item(name=name, description=description)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get("/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
