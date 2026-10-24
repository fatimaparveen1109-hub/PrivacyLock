let cart=[];
function money(n){return "Rs. "+Number(n).toLocaleString("en-PK")}
function renderProducts(products){
 const root=document.querySelector("#product-list");if(!root)return;
 const icons={"Shoes":"👟","Clothing":"👕","Accessories":"🎒"};
 root.innerHTML=products.map(p=>`<article class="product-card"><div class="product-art">${icons[p.category]||"📦"}</div><span class="pill">${escapeHtml(p.category)}</span><h3>${escapeHtml(p.name)}</h3><p class="muted">${p.stock} available</p><strong>${money(p.price)}</strong><button class="btn small-btn" data-add="${p.id}">Add to cart</button></article>`).join("");
 root.querySelectorAll("[data-add]").forEach(b=>b.addEventListener("click",()=>{const p=products.find(x=>x.id===Number(b.dataset.add));const old=cart.find(x=>x.id===p.id);if(old)old.quantity++;else cart.push({...p,quantity:1});renderCart()}));
}
function renderCart(){
 const root=document.querySelector("#cart-items");if(!root)return;
 root.innerHTML=cart.length?cart.map(x=>`<p>${escapeHtml(x.name)} × ${x.quantity} — ${money(x.price*x.quantity)} <button class="btn secondary small-btn" data-remove="${x.id}">Remove</button></p>`).join(""):"<p class='muted'>Your cart is empty.</p>";
 root.querySelectorAll("[data-remove]").forEach(b=>{b.onclick=()=>{cart=cart.filter(x=>x.id!==Number(b.dataset.remove));renderCart()}});
 const total=cart.reduce((s,x)=>s+x.price*x.quantity,0);document.querySelector("#cart-total").textContent=money(total);
}
async function loadOrders(){
 const root=document.querySelector("#orders-list");if(!root)return;
 try{const orders=await api("/api/orders/mine");root.innerHTML=orders.length?orders.map(o=>`<div class="panel"><strong>${escapeHtml(o.delivery_id)}</strong> · ${escapeHtml(o.product_name)} × ${o.quantity}<p>Status: <span class="pill">${escapeHtml(o.status)}</span> · Payment: ${escapeHtml(o.payment_status)}</p><p>Total: ${money(o.total)}</p>${o.payment_status!=="Verified (demo)"?`<button class="btn small-btn" data-pay="${escapeHtml(o.delivery_id)}">Pay now (demo)</button>`:""}${o.qr_active?`<p>Mock pickup token (demo only):</p><div class="qr-token">${escapeHtml(o.pickup_token||"")}</div>`:""}</div>`).join(""):"<p class='muted'>No orders yet.</p>";
 root.querySelectorAll("[data-pay]").forEach(b=>b.onclick=async()=>{try{await api(`/api/orders/${encodeURIComponent(b.dataset.pay)}/pay-demo`,{method:"POST"});await loadOrders()}catch(e){alert(e.message)}});
 }catch(e){root.innerHTML=`<p class="danger">${escapeHtml(e.message)}. Please log in again.</p>`}
}
document.addEventListener("DOMContentLoaded",async()=>{
 const session=getSession();if(!session||session.user.role!=="customer"){location.href="customer-login.html";return}
 document.querySelectorAll("[data-user-name]").forEach(e=>e.textContent=session.user.name);
 const list=document.querySelector("#product-list");
 if(list){try{renderProducts(await api("/api/products"))}catch(e){setMessage(document.querySelector("#customer-message"),"API not connected. Start the backend and refresh this page.",true)}}
 const orderForm=document.querySelector("#checkout-form");
 if(orderForm)orderForm.addEventListener("submit",async e=>{
  e.preventDefault();const msg=document.querySelector("#customer-message");if(!cart.length){setMessage(msg,"Please add a product to your cart first.",true);return}
  const preferred=document.querySelector("#preferred-hub").value;const alternative=document.querySelector("#alternative-hub").value;const payNow=document.querySelector("#pay-now").checked;
  try{
   for(const item of cart){await api("/api/orders",{method:"POST",body:JSON.stringify({product_id:item.id,quantity:item.quantity,preferred_hub:preferred,alternative_hub:alternative,pay_now:payNow})})}
   cart=[];renderCart();setMessage(msg,"Order placed in the demo system. Open My Orders to see tracking and payment details.");await loadOrders();
  }catch(err){setMessage(msg,err.message,true)}
 });
 document.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{document.querySelectorAll("[data-view]").forEach(v=>v.classList.add("hidden"));document.querySelector(`[data-view="${b.dataset.tab}"]`)?.classList.remove("hidden");document.querySelectorAll("[data-tab]").forEach(x=>x.classList.toggle("active",x===b));if(b.dataset.tab==="orders")loadOrders()});
 document.querySelectorAll("[data-logout]").forEach(b=>b.onclick=logout);
 renderCart();await loadOrders();
});
