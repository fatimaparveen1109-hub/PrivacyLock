document.addEventListener("DOMContentLoaded",()=>{
  const loginForm=document.querySelector("[data-login-form]");
  if(loginForm)loginForm.addEventListener("submit",async e=>{
    e.preventDefault(); const msg=document.querySelector("#form-message");
    const role=loginForm.dataset.role;
    const identifier=document.querySelector("#identifier").value.trim();
    const password=document.querySelector("#password").value;
    try{
      const data=await api("/api/auth/login",{method:"POST",body:JSON.stringify({identifier,password,role})});
      saveSession(data); const pages={customer:"customer-dashboard.html",seller:"seller-dashboard.html",rider:"rider-dashboard.html",admin:"admin-dashboard.html"};
      location.href=pages[role];
    }catch(err){setMessage(msg,err.message,true)}
  });
  const registerForm=document.querySelector("[data-register-form]");
  if(registerForm)registerForm.addEventListener("submit",async e=>{
    e.preventDefault();const msg=document.querySelector("#form-message");
    const name=document.querySelector("#name").value.trim();
    const email=document.querySelector("#email").value.trim();
    const phone=document.querySelector("#phone").value.trim();
    const password=document.querySelector("#password").value;
    const confirm=document.querySelector("#confirm-password").value;
    if(password.length<8){setMessage(msg,"Password must be at least 8 characters.",true);return}
    if(password!==confirm){setMessage(msg,"Passwords do not match.",true);return}
    try{const data=await api("/api/auth/register",{method:"POST",body:JSON.stringify({name,email,phone,password})});setMessage(msg,`${data.message} Your Customer ID is ${data.customer_id}.`);registerForm.reset()}
    catch(err){setMessage(msg,err.message,true)}
  });
});
