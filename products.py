from fastapi import APIRouter
from ..database import connect

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("")
def products():
    with connect() as con:
        rows = con.execute("SELECT id,name,category,price,stock FROM products ORDER BY id").fetchall()
    return [dict(row) for row in rows]
