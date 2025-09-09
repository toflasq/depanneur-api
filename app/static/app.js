const chat = document.getElementById('chat');
const qinput = document.getElementById('q');
const send = document.getElementById('send');

function appendMessage(text, cls){
  const d = document.createElement('div');
  d.className = 'message ' + cls;
  d.innerHTML = text;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

async function askServer(question){
  appendMessage("👤 " + question, "user");
  appendMessage("…loading", "bot");
  try {
    const res = await fetch('/api/ask', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({question})
    });
    const data = await res.json();
    // remove last loading message
    const msgs = chat.getElementsByClassName('bot');
    if (msgs.length) msgs[msgs.length-1].remove();

    if (data.results && data.results.length){
      let html = `<strong>${data.answer}</strong><br/>`;
      data.results.forEach(r=>{
        html += `<div><em>${r.device} — ${r.scenario || ''}</em><ul>`;
        (r.quick_checks||[]).slice(0,6).forEach(i=> html += `<li>${i}</li>`);
        html += `</ul></div>`;
      });
      appendMessage(html, "bot");
    } else {
      appendMessage("🤖 " + (data.answer || "Pas de réponse."), "bot");
    }
  } catch(e){
    appendMessage("Erreur réseau ou serveur.", "bot");
  }
}

send.addEventListener('click', ()=> {
  const q = qinput.value.trim();
  if (!q) return;
  askServer(q);
  qinput.value = '';
});

qinput.addEventListener('keydown', (e)=>{
  if (e.key === 'Enter') {
    e.preventDefault();
    send.click();
  }
});
