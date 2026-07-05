import re

HTML_FILE = "convite_maite_4anos.html"

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

log = []

if "rsvp-card{" not in html:
    css = """
<style>
  .rsvp-card{
    background: var(--white);
    border-radius: var(--radius-lg);
    padding: 22px 18px;
    box-shadow: var(--shadow-pink);
    border: 2px solid var(--pink-100);
  }
  .rsvp-card input{
    width:100%; font-family:'Quicksand', sans-serif; font-size:1rem;
    padding:12px 14px; border-radius:14px; border:2px solid var(--pink-200);
    background: var(--pink-50); color: var(--ink); margin-bottom:12px;
  }
  .rsvp-card input:focus{ outline:none; border-color: var(--pink-500); background:#fff; }
  .rsvp-card .rsvp-btn:disabled{ opacity:0.7; }
</style>
</head>"""
    html = html.replace("</head>", css, 1)
    log.append("✓ CSS do formulário adicionado")

old_section = re.search(r'<section class="rsvp reveal">.*?</section>', html, re.DOTALL)
if old_section:
    new_section = """<section class="rsvp reveal">
  <div class="rsvp-card">
    <input type="text" id="rsvpNome" placeholder="Seu nome">
    <input type="tel" id="rsvpTelefone" placeholder="Seu WhatsApp (com DDD)">
    <button type="button" class="rsvp-btn" id="rsvpBtn">Confirmar presença</button>
    <p class="rsvp-note" id="rsvpStatus">Preenche seu nome e WhatsApp pra confirmar</p>
  </div>
</section>"""
    html = html.replace(old_section.group(0), new_section, 1)
    log.append("✓ Formulário de confirmação de presença instalado")
else:
    log.append("⚠ Não encontrei a seção de RSVP pra trocar")

if "firebase-firestore.js" not in html:
    firebase_script = """
<script type="module">
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getFirestore, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "COLE_AQUI_SUA_API_KEY",
  authDomain: "COLE_AQUI.firebaseapp.com",
  projectId: "COLE_AQUI",
  storageBucket: "COLE_AQUI.appspot.com",
  messagingSenderId: "COLE_AQUI",
  appId: "COLE_AQUI"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const rsvpBtn = document.getElementById('rsvpBtn');
const rsvpStatus = document.getElementById('rsvpStatus');

if(rsvpBtn){
  rsvpBtn.addEventListener('click', async function(){
    const nome = document.getElementById('rsvpNome').value.trim();
    const telefone = document.getElementById('rsvpTelefone').value.trim();

    if(!nome || !telefone){
      rsvpStatus.textContent = 'Preenche seu nome e WhatsApp antes de confirmar :)';
      rsvpStatus.style.color = '#BE185D';
      return;
    }

    rsvpBtn.disabled = true;
    rsvpBtn.textContent = 'Confirmando...';

    try{
      await addDoc(collection(db, 'rsvps_maite4anos'), {
        nome: nome,
        telefone: telefone,
        confirmadoEm: serverTimestamp()
      });
      rsvpStatus.textContent = 'Presença confirmada! Já avisamos a família da Maitê';
      rsvpStatus.style.color = '#16A34A';
      rsvpBtn.textContent = 'Confirmado';
    }catch(err){
      console.error(err);
      rsvpStatus.textContent = 'Ops, algo deu errado. Tenta de novo em alguns segundos.';
      rsvpStatus.style.color = '#DC2626';
      rsvpBtn.disabled = false;
      rsvpBtn.textContent = 'Confirmar presença';
    }
  });
}
</script>
</body>"""
    html = html.replace("</body>", firebase_script, 1)
    log.append("✓ Conexão com o Firebase adicionada")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("\n".join(log))
