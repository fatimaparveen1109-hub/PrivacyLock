document.addEventListener("DOMContentLoaded",()=>{
 const s=getSession();if(!s||s.user.role!=="rider"){location.href="rider-login.html";return}
 document.querySelectorAll("[data-user-name]").forEach(e=>e.textContent=s.user.name);
 document.querySelectorAll("[data-logout]").forEach(b=>b.onclick=logout);
});
