from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import auth, products, orders

app = FastAPI(title="PrivacyLock Demo API", version="0.1.0",
              description="University prototype API. Do not deploy publicly without security hardening.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local demo only; restrict to deployed frontend origin in production.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"status":"ok","project":"PrivacyLock","mode":"local-demo"}

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
