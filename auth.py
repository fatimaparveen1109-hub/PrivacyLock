from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..database import connect
from ..security import make_token, demo_password_hash

router = APIRouter(prefix="/api/auth", tags=["authentication"])
# Local demo sessions only; sessions reset when server restarts.
SESSIONS = {}

class LoginInput(BaseModel):
    identifier: str
    password: str
    role: str

class RegisterInput(BaseModel):
    name: str
    email: EmailStr
    phone: str = ""
    password: str

@router.post("/login")
def login(data: LoginInput):
    role = data.role.lower()
    if role not in {"customer","seller","rider","admin"}:
        raise HTTPException(400, "Invalid role")
    with connect() as con:
        user = con.execute(
            "SELECT * FROM users WHERE role=? AND (email=? OR display_id=?)",
            (role, data.identifier, data.identifier)
        ).fetchone()
    if not user or user["password"] != data.password:
        raise HTTPException(401, "Email/ID or password is incorrect")
    if not user["approved"]:
        raise HTTPException(403, "This account is waiting for Admin approval")
    token = make_token()
    SESSIONS[token] = {"id": user["id"], "display_id": user["display_id"], "name": user["name"],
                       "email": user["email"], "role": user["role"]}
    return {"token": token, "user": SESSIONS[token]}

@router.post("/register")
def register(data: RegisterInput):
    with connect() as con:
        if con.execute("SELECT 1 FROM users WHERE email=?", (data.email,)).fetchone():
            raise HTTPException(409, "An account with this email already exists")
        display_id = f"CUS-{1001 + con.execute('SELECT COUNT(*) FROM users WHERE role=?', ('customer',)).fetchone()[0]}"
        con.execute(
            "INSERT INTO users(display_id,name,email,password,role,approved) VALUES(?,?,?,?,?,1)",
            (display_id, data.name, data.email, data.password, "customer")
        )
        user = con.execute("SELECT id,display_id,name,email,role FROM users WHERE email=?", (data.email,)).fetchone()
    return {"message":"Account created. Please log in.", "customer_id":user["display_id"]}

def current_user(authorization: str | None):
    if not authorization:
        raise HTTPException(401, "Please log in first")
    token = authorization.removeprefix("Bearer ").strip()
    user = SESSIONS.get(token)
    if not user:
        raise HTTPException(401, "Session expired. Please log in again.")
    return user
