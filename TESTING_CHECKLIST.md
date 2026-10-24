# PrivacyLock Starter — Testing Checklist

- [ ] Start API using `uvicorn backend.app.main:app --reload`.
- [ ] Open `http://127.0.0.1:8000/api/health` and confirm status is `ok`.
- [ ] Open `http://127.0.0.1:8000/docs` and inspect API endpoints.
- [ ] Open `frontend/index.html`.
- [ ] Register a customer and then log in.
- [ ] Add products to cart and place a demo order.
- [ ] Confirm payment-at-order produces a mock pickup token.
- [ ] Confirm payment-due order can use the demo Pay Now action.
- [ ] Log in with demo Seller/Rider/Admin accounts.
- [ ] Check the limitations in README before presenting or deploying.
