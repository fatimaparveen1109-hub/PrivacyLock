const API_BASE = localStorage.getItem("privacylock_api") || "http://127.0.0.1:8000";
function setMessage(el, text, isError=false){ if(!el)return; el.textContent=text; el.classList.remove("hidden","error"); if(isError)el.classList.add("error"); }
function escapeHtml(value){return String(value ?? "").replace(/[&<>"']/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function getSession(){try{return JSON.parse(sessionStorage.getItem("privacylock_session")||"null")}catch{return null}}
function saveSession(data){sessionStorage.setItem("privacylock_session",JSON.stringify(data))}
function logout(){sessionStorage.removeItem("privacylock_session");location.href="index.html"}
async function api(path, options={}) {
  const session=getSession();
  const headers={"Content-Type":"application/json",...(options.headers||{})};
  if(session?.token)headers.Authorization=`Bearer ${session.token}`;
  const response=await fetch(`${API_BASE}${path}`,{...options,headers});
  const body=await response.json().catch(()=>({detail:"The server did not return JSON"}));
  if(!response.ok)throw new Error(body.detail||"Request failed");
  return body;
}
