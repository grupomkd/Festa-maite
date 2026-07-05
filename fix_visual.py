import re

HTML_FILE = "convite_maite_4anos.html"

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

log = []

# 1) SKYE DO ENVELOPE APARECENDO APAGADA -> deixa opacidade total
def boost_opacity(match):
    tag = match.group(0)
    if 'style="' in tag:
        return tag.replace('style="', 'style="opacity:1 !important;', 1)
    return tag

pattern = re.compile(r'<img class="env-decor paw[12]"[^>]*>')
new_html, n = pattern.subn(boost_opacity, html)
if n > 0:
    html = new_html
    log.append(f"✓ Opacidade da Skye no envelope corrigida ({n} imagens)")
else:
    log.append("⚠ Não encontrei as imagens da Skye no envelope pra corrigir opacidade")

# 2) RECONSTRUIR A SEÇÃO "DEIXE UM CARINHO" DO ZERO, BONITA E BLINDADA (nao depende de CSS externo)
section_pattern = re.compile(r'<section[^>]*>(?:(?!</section>).)*?carinho(?:(?!</section>).)*?</section>', re.DOTALL | re.IGNORECASE)
new_section = '''<section style="margin:30px 20px 0;background:linear-gradient(160deg,#ffffff,#FDF2F8);border-radius:28px;padding:24px 18px;box-shadow:0 12px 30px rgba(219,39,119,0.25);border:2px solid #FCE7F3;">
  <h3 style="margin:0 0 4px;color:#BE185D;font-size:1.25rem;text-align:center;font-family:'Baloo 2',cursive,sans-serif;">Deixe um carinho pra Maitê</h3>
  <p style="margin:0 0 18px;text-align:center;font-size:0.9rem;color:#8a5570;font-family:'Quicksand',sans-serif;">Escreva uma mensagem de aniversário! Ela vai adorar ler.</p>
  <input type="text" id="msgName" placeholder="Seu nome" style="width:100%;box-sizing:border-box;font-family:'Quicksand',sans-serif;font-size:1rem;padding:13px 16px;border-radius:14px;border:2px solid #FBCFE8;background:#fff;color:#5B1436;margin-bottom:12px;outline:none;">
  <textarea id="msgText" rows="3" placeholder="Escreva sua mensagem para a Maitê..." style="width:100%;box-sizing:border-box;font-family:'Quicksand',sans-serif;font-size:1rem;padding:13px 16px;border-radius:14px;border:2px solid #FBCFE8;background:#fff;color:#5B1436;margin-bottom:14px;resize:vertical;outline:none;"></textarea>
  <button type="button" id="sendMsgBtn" style="width:100%;min-height:48px;border:none;border-radius:999px;background:linear-gradient(135deg,#F472B6,#DB2777);color:#fff;font-family:'Baloo 2',cursive,sans-serif;font-weight:700;font-size:1rem;cursor:pointer;">Enviar mensagem</button>
</section>'''

if section_pattern.search(html):
    html = section_pattern.sub(new_section, html, count=1)
    log.append("✓ Seção de mensagem reconstruída, bonita e independente do CSS antigo")
else:
    log.append("⚠ Não encontrei a seção de mensagem para reconstruir")

# 3) GARANTIR QUE O BOTAO DE ENVIAR MENSAGEM FUNCIONA (reforca o listener, mesmo se ja existir outro)
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
    log.append("✓ Garantia extra de funcionamento do botão de mensagem adicionada")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("\n".join(log))
