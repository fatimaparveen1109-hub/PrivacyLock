# PrivacyLock — Complete Starter Project

**Official title:** Privacy-Based Automated Parcel Locker Delivery System  
**Tagline:** Your Parcel. Your Privacy. Your Convenience.

This is a starter implementation containing:
- Responsive HTML/CSS/JavaScript frontend pages for Welcome, Customer, Seller, Rider and Admin.
- Python + FastAPI backend with demo authentication, product catalogue, orders, payments simulation, tracking, and role-aware endpoints.
- SQLite for quick local demonstration only. The database layer is kept simple so it can be migrated to cloud PostgreSQL for deployment.
- Mock QR/pickup flow only. It does **not** open a real physical locker and is not connected to the other group's QR system.

## Requirements
- Python 3.10+
- A modern browser
- Internet is not needed to run the local starter once Python dependencies are installed.

## Run on Windows
1. Extract the ZIP.
2. Open the extracted `PrivacyLock_Complete_Starter` folder.
3. Open a terminal/Command Prompt in that folder.
4. Install backend requirements:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r backend/requirements.txt
   ```
5. Start the backend:
   ```bash
   uvicorn backend.app.main:app --reload
   ```
6. Open `frontend/index.html` in a browser. Keep the backend running for API-connected demo actions.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```
Then open `frontend/index.html` in a browser.

## Demo accounts
For a classroom-only demo, the backend creates these accounts on first startup:
- Admin: `admin@privacylock.demo` / `AdminDemo123!`
- Seller: `SELLER-1001` / `SellerDemo123!`
- Rider: `RIDER-1001` / `RiderDemo123!`
- Customer: create an account using the Customer Register page.

**Change demo passwords before any shared or deployed use.** These credentials are intentionally for local demo only.

## Important limitations
- Payments are simulated; no money is charged.
- The QR code shown in the demo is a mock text/token flow, not a production secure QR implementation.
- No real email/SMS notifications are sent.
- SQLite is for local prototype testing only, not production cloud deployment.
- No physical locker commands are sent.
- Do not deploy this starter publicly with demo credentials or without additional security review.

## Project structure
```text
PrivacyLock_Complete_Starter/
  frontend/
    index.html
    customer-login.html
    customer-register.html
    seller-login.html
    seller-register.html
    rider-login.html
    admin-login.html
    customer-dashboard.html
    seller-dashboard.html
    rider-dashboard.html
    admin-dashboard.html
    css/styles.css
    css/dashboard.css
    js/main.js
    js/auth.js
    js/customer.js
    js/seller.js
    js/rider.js
    js/admin.js
  backend/
    app/main.py
    app/database.py
    app/security.py
    app/routers/auth.py
    app/routers/products.py
    app/routers/orders.py
    requirements.txt
    .env.example
  .gitignore
```
