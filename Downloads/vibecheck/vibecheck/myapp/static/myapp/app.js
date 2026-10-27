const sid=localStorage.sid||(localStorage.sid=Math.random().toString(36).slice(2));
const $=id=>document.getElementById(id),box=$("chat"),msgs=$("chat-msgs");
const openChat=()=>{box.hidden=false;$("chat-input").focus()};
$("chat-toggle").onclick=()=>box.hidden?openChat():box.hidden=true;$("chat-close").onclick=()=>box.hidden=true;
document.querySelectorAll(".open-chat").forEach(b=>b.onclick=openChat);
function add(cls,text){const d=document.createElement("div");d.className=cls;d.textContent=text;msgs.append(d);msgs.scrollTop=msgs.scrollHeight;return d}
async function send(){const i=$("chat-input"),m=i.value.trim();if(!m)return;i.value="";add("me",m);
 try{const r=await fetch("/api/chat/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:m,session:sid})});
  const d=await r.json();add("bot",d.reply||"Sorry, something went wrong.");
  const f=add("fb","");for(const [l,v] of [["👍",true],["👎",false]]){const b=document.createElement("button");b.textContent=l;
   b.onclick=()=>{fetch("/api/feedback/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:m,helpful:v,session:sid})});f.textContent="Thanks for the feedback!"};f.append(b)}
 }catch(e){add("bot","Network error. Please try again.")}}
$("chat-send").onclick=send;$("chat-input").onkeydown=e=>{if(e.key==="Enter")send()};
if(location.search.includes("chat=open"))openChat();
// particles
const c=$("particles"),x=c.getContext("2d");let P=[];
function rs(){c.width=innerWidth;c.height=innerHeight;P=Array.from({length:50},()=>({x:Math.random()*c.width,y:Math.random()*c.height,r:Math.random()*2+1,s:Math.random()*.6+.2}))}
rs();addEventListener("resize",rs);
(function loop(){x.clearRect(0,0,c.width,c.height);x.fillStyle=getComputedStyle(document.body).getPropertyValue("--accent");x.globalAlpha=.35;
 P.forEach(p=>{p.y-=p.s;if(p.y<0)p.y=c.height;x.beginPath();x.arc(p.x,p.y,p.r,0,7);x.fill()});requestAnimationFrame(loop)})();
