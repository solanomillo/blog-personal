(function(){
  const toggle = document.getElementById('chat-toggle');
  const panel = document.getElementById('chat-panel');
  const closeBtn = document.getElementById('chat-close');
  const messages = document.getElementById('chat-messages');
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send');
  let greeted = false;

  function appendMessage(role, content, isHtml=false){
    const el = document.createElement('div');
    el.className = 'msg ' + (role==='user'?'user':'bot');
    if(isHtml){ el.innerHTML = content; } else { el.textContent = content; }
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  function openPanel(){
    panel.hidden=false;
    if(!greeted){
      fetch(`/chat/ask/?message=__init__`)
        .then(r=>r.json())
        .then(data=>{ appendMessage('bot', data.respuesta, true); greeted=true; })
        .catch(err=>console.error(err));
    }
  }

  function closePanel(){ panel.hidden=true; }

  function sendMessage(){
    const text=input.value.trim();
    if(!text) return;
    appendMessage('user', text, false);
    input.value='';
    const loaderId='loader-'+Date.now();
    appendMessage('bot','Escribiendo...', false);
    messages.lastChild.id=loaderId;

    fetch(`/chat/ask/?message=${encodeURIComponent(text)}`)
      .then(r=>r.json())
      .then(data=>{
        const loaderEl=document.getElementById(loaderId); if(loaderEl) loaderEl.remove();
        appendMessage('bot', data.respuesta, true);
      })
      .catch(err=>{
        const loaderEl=document.getElementById(loaderId); if(loaderEl) loaderEl.remove();
        appendMessage('bot','Lo siento, hubo un error al consultar el servidor.', false);
        console.error(err);
      });
  }

  toggle.addEventListener('click', ()=>{ if(panel.hidden) openPanel(); else closePanel(); });
  closeBtn.addEventListener('click', closePanel);
  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keypress',(e)=>{ if(e.key==='Enter') sendMessage(); });
})();
