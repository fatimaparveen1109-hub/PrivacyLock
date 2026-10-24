import json
import os
import sqlite3
from pathlib import Path

DB_PATH = os.getenv("PRIVACYLOCK_DB", str(Path(__file__).resolve().parents[2] / "privacylock_demo.db"))

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            approved INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            seller_id INTEGER
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_id TEXT UNIQUE NOT NULL,
            customer_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            payment_status TEXT NOT NULL,
            status TEXT NOT NULL,
            preferred_hub TEXT NOT NULL,
            alternative_hub TEXT NOT NULL,
            pickup_token TEXT,
            qr_active INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)
        count = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            # Demo-only plaintext passwords; replace with proper password hashing before deployment.
            con.executemany(
                "INSERT INTO users(display_id,name,email,password,role,approved) VALUES(?,?,?,?,?,?)",
                [
                    ("ADM-1001","Demo Admin","admin@privacylock.demo","AdminDemo123!","admin",1),
                    ("SELLER-1001","Demo Seller","seller@privacylock.demo","SellerDemo123!","seller",1),
                    ("RIDER-1001","Demo Rider","rider@privacylock.demo","RiderDemo123!","rider",1),
                ],
            )
        pcount = con.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if pcount == 0:
            seller_id = con.execute("SELECT id FROM users WHERE role='seller' LIMIT 1").fetchone()[0]
            con.executemany(
                "INSERT INTO products(name,category,price,stock,seller_id) VALUES(?,?,?,?,?)",
                [
                    ("Everyday Sneakers","Shoes",2499,12,seller_id),
                    ("Classic T-Shirt","Clothing",899,25,seller_id),
                    ("Canvas Backpack","Accessories",1799,8,seller_id),
                    ("Casual Hoodie","Clothing",2199,10,seller_id),
                ],
            )
