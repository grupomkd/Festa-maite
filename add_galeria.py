import re

HTML_FILE = "convite_maite_4anos.html"

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

log = []

# 1) REMOVER TODAS AS SECOES DE MENSAGEM DUPLICADAS E DEIXAR SO UMA, BONITA
section_pattern = re.compile(r'<section[^>]*>(?:(?!</section>).)*?carinho(?:(?!</section>).)*?</section>', re.DOTALL | re.IGNORECASE)
matches = section_pattern.findall(html)
count_found = len(section_pattern.findall(html))

clean_section = '''<section style="margin:30px 20px 0;background:linear-gradient(160deg,#ffffff,#FDF2F8);border-radius:28px;padding:24px 18px;box-shadow:0 12px 30px rgba(219,39,119,0.25);border:2px solid #FCE7F3;">
  <h3 style="margin:0 0 4px;color:#BE185D;font-size:1.25rem;text-align:center;font-family:'Baloo 2',cursive,sans-serif;">Deixe um carinho pra Maitê</h3>
  <p style="margin:0 0 18px;text-align:center;font-size:0.9rem;color:#8a5570;font-family:'Quicksand',sans-serif;">Escreva uma mensagem de aniversário! Ela vai adorar ler.</p>
  <input type="text" id="msgName" placeholder="Seu nome" style="width:100%;box-sizing:border-box;font-family:'Quicksand',sans-serif;font-size:1rem;padding:13px 16px;border-radius:14px;border:2px solid #FBCFE8;background:#fff;color:#5B1436;margin-bottom:12px;outline:none;">
  <textarea id="msgText" rows="3" placeholder="Escreva sua mensagem para a Maitê..." style="width:100%;box-sizing:border-box;font-family:'Quicksand',sans-serif;font-size:1rem;padding:13px 16px;border-radius:14px;border:2px solid #FBCFE8;background:#fff;color:#5B1436;margin-bottom:14px;resize:vertical;outline:none;"></textarea>
  <button type="button" id="sendMsgBtn" style="width:100%;min-height:48px;border:none;border-radius:999px;background:linear-gradient(135deg,#F472B6,#DB2777);color:#fff;font-family:'Baloo 2',cursive,sans-serif;font-weight:700;font-size:1rem;cursor:pointer;">Enviar mensagem</button>
</section>'''

if count_found >= 1:
    # remove todas as ocorrencias
    html = section_pattern.sub('___MSG_PLACEHOLDER___', html)
    # troca so a primeira ocorrencia do placeholder pela versao limpa, remove as demais
    first_done = False
    parts = html.split('___MSG_PLACEHOLDER___')
    rebuilt = parts[0]
    for i, p in enumerate(parts[1:]):
        if not first_done:
            rebuilt += clean_section
            first_done = True
        rebuilt += p
    html = rebuilt
    log.append(f"✓ Encontradas {count_found} secao(oes) de mensagem — deixei so 1, limpa")
else:
    log.append("⚠ Nenhuma secao de mensagem encontrada")

# 2) GARANTIR O LISTENER DO BOTAO DE MENSAGEM
if "sendMsgBtn_v2_listener" not in html:
    js = '''
<script id="sendMsgBtn_v2_listener">
(function(){
  document.addEventListener('DOMContentLoaded', function(){
    var btn = document.getElementById('sendMsgBtn');
    if(!btn || btn.dataset.boundV2) return;
    btn.dataset.boundV2 = "1";
    btn.addEventListener('click', function(){
      var nameEl = document.getElementById('msgName');
      var msgEl = document.getElementById('msgText');
      var name = nameEl ? nameEl.value.trim() : '';
      var msg = msgEl ? msgEl.value.trim() : '';
      if(!name || !msg){ alert('Preenche seu nome e a mensagem antes de enviar :)'); return; }
      var text = encodeURIComponent('Mensagem para a Maite de ' + name + ': ' + msg);
      window.open('https://wa.me/?text=' + text, '_blank');
    });
  });
})();
</script>
</body>'''
    html = html.replace("</body>", js, 1)
    log.append("✓ Listener do botao de mensagem garantido")

# 3) ADICIONAR A GALERIA (fotos + videos) com lightbox simples
if 'id="galeriaMaite"' not in html:
    fotos = [f"galeria/maite_{i:02d}.jpg" for i in range(1, 15)]
    videos = [f"galeria/maite_video_{i:02d}.mp4" for i in range(1, 6)]

    thumbs_html = ""
    for i, foto in enumerate(fotos):
        thumbs_html += f'<img src="{foto}" loading="lazy" onclick="abrirLightbox(\'{foto}\', \'img\')" style="width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:14px;cursor:pointer;box-shadow:0 4px 10px rgba(190,24,93,0.18);">\n'
    for i, video in enumerate(videos):
        thumbs_html += f'''<div onclick="abrirLightbox('{video}', 'video')" style="position:relative;width:100%;aspect-ratio:1/1;border-radius:14px;overflow:hidden;cursor:pointer;box-shadow:0 4px 10px rgba(190,24,93,0.18);background:#000;">
  <video src="{video}" muted style="width:100%;height:100%;object-fit:cover;"></video>
  <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.25);">
    <svg width="36" height="36" viewBox="0 0 24 24" fill="#fff"><path d="M8 5v14l11-7z"/></svg>
  </div>
</div>
'''

    galeria_section = f'''<section id="galeriaMaite" style="margin:30px 20px 0;">
  <h3 style="margin:0 0 4px;color:#BE185D;font-size:1.3rem;text-align:center;font-family:'Baloo 2',cursive,sans-serif;">Galeria da Maitê</h3>
  <p style="margin:0 0 18px;text-align:center;font-size:0.9rem;color:#8a5570;font-family:'Quicksand',sans-serif;">Alguns momentos especiais dela</p>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;">
    {thumbs_html}
  </div>
</section>

<div id="lightboxOverlay" onclick="fecharLightbox()" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.9);z-index:2000;align-items:center;justify-content:center;padding:20px;">
  <div id="lightboxContent" style="max-width:100%;max-height:100%;"></div>
</div>

<script>
function abrirLightbox(src, tipo){{
  var overlay = document.getElementById('lightboxOverlay');
  var content = document.getElementById('lightboxContent');
  if(tipo === 'video'){{
    content.innerHTML = '<video src="' + src + '" controls autoplay style="max-width:100%;max-height:90vh;border-radius:10px;"></video>';
  }} else {{
    content.innerHTML = '<img src="' + src + '" style="max-width:100%;max-height:90vh;border-radius:10px;">';
  }}
  overlay.style.display = 'flex';
}}
function fecharLightbox(){{
  var overlay = document.getElementById('lightboxOverlay');
  overlay.style.display = 'none';
  document.getElementById('lightboxContent').innerHTML = '';
}}
</script>
</body>'''

    html = html.replace("</body>", galeria_section, 1)
    log.append(f"✓ Galeria adicionada ({len(fotos)} fotos + {len(videos)} videos)")
else:
    log.append("⚠ Galeria ja existe, nao dupliquei")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("\n".join(log))
