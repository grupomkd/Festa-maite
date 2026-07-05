import re

HTML_FILE = "convite_maite_4anos.html"

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

log = []

div_match = re.search(r'<div class="paw-divider"[^>]*>(.*?)</div>', html, re.DOTALL)
if div_match:
    inner = div_match.group(1)
    srcs = re.findall(r'src="(data:image/png;base64,[^"]+)"', inner)
    if len(srcs) >= 3:
        new_div = (
            '<div class="paw-divider skye-trio" aria-hidden="true">'
            f'<img src="{srcs[0]}" class="skye-trio-side">'
            f'<img src="{srcs[1]}" class="skye-trio-center">'
            f'<img src="{srcs[2]}" class="skye-trio-side skye-flip">'
            '</div>'
        )
        html = html.replace(div_match.group(0), new_div, 1)
        log.append("✓ Trio de Skye aumentado")
    else:
        log.append("⚠ Encontrei o bloco mas não as 3 imagens dentro dele")
else:
    log.append("⚠ Não encontrei o bloco paw-divider")

if "skye-trio-center" not in html.split("<style>")[-1]:
    extra_css = """
<style>
  .skye-trio{ display:flex; align-items:center; justify-content:center; gap:8px; padding:18px 0 8px; }
  .skye-trio img{ filter: drop-shadow(0 6px 10px rgba(190,24,93,0.28)); }
  .skye-trio-center{ width:100px !important; opacity:1 !important; z-index:2; }
  .skye-trio-side{ width:66px !important; opacity:1 !important; }
  .skye-flip{ transform: scaleX(-1); }

  .rsvp-btn{
    overflow:hidden;
    background: linear-gradient(135deg, var(--pink-500), var(--pink-700)) !important;
  }
  @keyframes pulseGlow{
    0%,100%{ box-shadow: 0 12px 26px rgba(190,24,93,0.4); }
    50%{ box-shadow: 0 16px 32px rgba(190,24,93,0.55); }
  }

  .msg-card{
    margin: 30px 20px 0;
    background: linear-gradient(160deg, var(--white), var(--pink-50));
    border-radius: var(--radius-lg);
    padding: 22px 18px;
    box-shadow: var(--shadow-pink);
    border: 2px solid var(--pink-100);
  }
  .msg-card h3{ margin:0 0 4px; color: var(--pink-700); font-size:1.2rem; text-align:center; }
  .msg-card p.sub{ margin:0 0 16px; text-align:center; font-size:0.85rem; color:#8a5570; }
  .msg-card input, .msg-card textarea{
    width:100%; font-family:'Quicksand', sans-serif; font-size:1rem;
    padding:12px 14px; border-radius:14px; border:2px solid var(--pink-200);
    background: var(--white); color: var(--ink); margin-bottom:12px; resize:vertical;
  }
  .msg-card input:focus, .msg-card textarea:focus{ outline:none; border-color: var(--pink-500); }
  .msg-card button{
    width:100%; min-height:48px; border:none; border-radius:999px;
    background: linear-gradient(135deg, var(--pink-400), var(--pink-600));
    color:#fff; font-family:'Baloo 2', cursive; font-weight:700; font-size:1rem;
  }
</style>
</head>"""
    html = html.replace("</head>", extra_css, 1)
    log.append("✓ CSS de ajustes inserido")

if 'class="msg-card reveal"' not in html:
    msg_section = """<section class="msg-card reveal">
  <h3>Deixe um carinho pra Maitê</h3>
  <p class="sub">Escreva uma mensagem de aniversário! Ela vai adorar ler.</p>
  <input type="text" id="msgName" placeholder="Seu nome">
  <textarea id="msgText" rows="3" placeholder="Escreva sua mensagem para a Maitê..."></textarea>
  <button type="button" id="sendMsgBtn">Enviar mensagem</button>
</section>

  <section class="rsvp reveal">"""
    if '<section class="rsvp reveal">' in html:
        html = html.replace('<section class="rsvp reveal">', msg_section, 1)
        log.append("✓ Seção de mensagem adicionada antes do RSVP")
    else:
        log.append("⚠ Não encontrei a seção de RSVP para inserir a mensagem antes dela")

if "confetti-layer-rsvp" not in html:
    extra_js = """
<script>
(function(){
  var btn = document.getElementById('sendMsgBtn');
  if(btn){
    btn.addEventListener('click', function(){
      var name = document.getElementById('msgName').value.trim();
      var msg = document.getElementById('msgText').value.trim();
      if(!name || !msg){ alert('Preenche seu nome e a mensagem antes de enviar :)'); return; }
      var text = encodeURIComponent('Mensagem para a Maite de ' + name + ': ' + msg);
      window.open('https://wa.me/?text=' + text, '_blank');
    });
  }

  var rsvp = document.querySelector('.rsvp-btn');
  if(rsvp){
    rsvp.addEventListener('click', function(){
      var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if(reduced) return;
      var layer = document.createElement('div');
      layer.id = 'confetti-layer-rsvp';
      layer.style.position='fixed'; layer.style.inset='0'; layer.style.zIndex='1000';
      layer.style.pointerEvents='none'; layer.style.overflow='hidden';
      document.body.appendChild(layer);
      var colors = ['#EC4899','#F472B6','#F9A8D4','#F4C55A','#BE185D'];
      for(var i=0;i<34;i++){
        var piece = document.createElement('div');
        piece.style.position='absolute';
        piece.style.top='-30px';
        piece.style.left = (Math.random()*100) + 'vw';
        piece.style.width='10px'; piece.style.height='14px';
        piece.style.borderRadius = (Math.random()>0.5 ? '50%' : '2px');
        piece.style.background = colors[Math.floor(Math.random()*colors.length)];
        piece.style.setProperty('--drift', (Math.random()*180-90)+'px');
        piece.style.setProperty('--spin', (Math.random()*540+180)+'deg');
        piece.style.animation = 'confettiFall ' + (1.4+Math.random()*1.2) + 's cubic-bezier(.3,.6,.4,1) forwards';
        piece.style.animationDelay = (Math.random()*0.4)+'s';
        layer.appendChild(piece);
      }
      setTimeout(function(){ layer.remove(); }, 3000);
    });
  }
})();
</script>
</body>"""
    html = html.replace("</body>", extra_js, 1)
    log.append("✓ Confete no clique + envio de mensagem adicionados")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("\n".join(log))
