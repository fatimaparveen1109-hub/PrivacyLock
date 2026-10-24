import secrets
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from ..database import connect
from .auth import current_user

router = APIRouter(prefix="/api/orders", tags=["orders"])

class OrderInput(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=20)
    preferred_hub: str
    alternative_hub: str
    pay_now: bool = True

@router.post("")
def create_order(data: OrderInput, authorization: str | None = Header(default=None)):
    user = current_user(authorization)
    if user["role"] != "customer":
        raise HTTPException(403, "Only customers can place orders")
    with connect() as con:
        product = con.execute("SELECT * FROM products WHERE id=?", (data.product_id,)).fetchone()
        if not product:
            raise HTTPException(404, "Product not found")
        if product["stock"] < data.quantity:
            raise HTTPException(409, "Not enough stock available")
        total = product["price"] * data.quantity
        payment_status = "Verified (demo)" if data.pay_now else "Payment Due"
        status = "Order Placed" if data.pay_now else "Payment Pending"
        delivery_id = "PL-" + secrets.token_hex(4).upper()
        token = secrets.token_urlsafe(16) if data.pay_now else None
        con.execute("UPDATE products SET stock=stock-? WHERE id=?", (data.quantity, data.product_id))
        con.execute("""INSERT INTO orders(delivery_id,customer_id,product_name,quantity,total,payment_status,
                       status,preferred_hub,alternative_hub,pickup_token,qr_active)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                    (delivery_id,user["id"],product["name"],data.quantity,total,payment_status,status,
                     data.preferred_hub,data.alternative_hub,token,1 if data.pay_now else 0))
        order_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]
        con.execute("INSERT INTO events(order_id,message) VALUES(?,?)", (order_id,"Order created in demo system"))
    return {"delivery_id":delivery_id,"product":product["name"],"quantity":data.quantity,
            "total":total,"payment_status":payment_status,"status":status,
            "pickup_qr_token":token,"qr_active":bool(data.pay_now),
            "notice":"Demo only: this token does not unlock a physical locker."}

@router.get("/mine")
def my_orders(authorization: str | None = Header(default=None)):
    user = current_user(authorization)
    with connect() as con:
        if user["role"] == "customer":
            rows = con.execute("SELECT * FROM orders WHERE customer_id=? ORDER BY id DESC", (user["id"],)).fetchall()
        elif user["role"] == "admin":
            rows = con.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        else:
            raise HTTPException(403, "This role cannot view the customer order list")
    return [dict(r) for r in rows]

@router.post("/{delivery_id}/pay-demo")
def pay_demo(delivery_id: str, authorization: str | None = Header(default=None)):
    user = current_user(authorization)
    if user["role"] != "customer":
        raise HTTPException(403, "Only customers can pay")
    with connect() as con:
        order = con.execute("SELECT * FROM orders WHERE delivery_id=? AND customer_id=?",
                            (delivery_id,user["id"])).fetchone()
        if not order:
            raise HTTPException(404, "Order not found")
        token = order["pickup_token"] or secrets.token_urlsafe(16)
        con.execute("UPDATE orders SET payment_status='Verified (demo)', status='Order Placed', pickup_token=?, qr_active=1 WHERE id=?",
                    (token,order["id"]))
    return {"message":"Demo payment marked successful","pickup_qr_token":token,
            "notice":"Mock token only; not a physical locker unlock credential."}
