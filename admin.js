document.addEventListener("DOMContentLoaded",async()=>{
 const s=getSession();if(!s||s.user.role!=="admin"){location.href="admin-login.html";return}
 document.querySelectorAll("[data-user-name]").forEach(e=>e.textContent=s.user.name);
 document.querySelectorAll("[data-logout]").forEach(b=>b.onclick=logout);
 const root=document.querySelector("#admin-orders");
 try{const orders=await api("/api/orders/mine");if(root)root.innerHTML=orders.length?`<div class="table-wrap"><table><thead><tr><th>Delivery ID</th><th>Product</th><th>Total</th><th>Payment</th><th>Status</th></tr></thead><tbody>${orders.map(o=>`<tr><td>${escapeHtml(o.delivery_id)}</td><td>${escapeHtml(o.product_name)}</td><td>Rs. ${Number(o.total).toLocaleString()}</td><td>${escapeHtml(o.payment_status)}</td><td>${escapeHtml(o.status)}</td></tr>`).join("")}</tbody></table></div>`:"<p>No orders yet.</p>"}catch(e){if(root)root.textContent=e.message}
});
