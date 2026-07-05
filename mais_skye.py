import base64, re

HTML_FILE = "convite_maite_4anos.html"

def to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

b64_voando = to_base64("skye_voando.png")
b64_sentada = to_base64("skye_sentada.png")
b64_dinamica = to_base64("skye_dinamica.png")
b64_correndo = to_base64("skye_correndo.png")

changes = 0

# 1) AUMENTAR O SELO DO ENVELOPE (deixa a imagem quase do tamanho do círculo todo)
new_css = """
<style>
  /* ===== SKYE EM DESTAQUE ===== */
  .seal{ width:46% !important; }
  .seal img{ width:92% !important; height:92% !important; }
  .photo-frame .paw-badge{ width:92px !important; height:92px !important; }
  .photo-frame .paw-badge img{ width:96% !important; height:96% !important; }
</style>
</head>"""
if "</head>" in html and "SKYE EM DESTAQUE" not in html:
    html = html.replace("</head>", new_css, 1)
    changes += 1
    print("✓ Selo e crachá aumentados")

# 2) PATINHAS FLUTUANTES DO ENVELOPE -> SKYE DE VERDADE, MAIOR
old_paw1 = '<svg class="env-decor paw1" viewBox="0 0 100 100" fill="#BE185D"><ellipse cx="50" cy="62" rx="28" ry="24"/><ellipse cx="18" cy="30" rx="12" ry="15"/><ellipse cx="45" cy="14" rx="12" ry="15"/><ellipse cx="72" cy="18" rx="11" ry="14"/><ellipse cx="88" cy="42" rx="11" ry="14"/></svg>'
new_paw1 = f'<img class="env-decor paw1" style="width:110px;" src="data:image/png;base64,{b64_dinamica}" alt="Skye">'
if old_paw1 in html:
    html = html.replace(old_paw1, new_paw1, 1)
    changes += 1
    print("✓ Patinha 1 do envelope virou Skye")

old_paw2 = '<svg class="env-decor paw2" viewBox="0 0 100 100" fill="#BE185D"><ellipse cx="50" cy="62" rx="28" ry="24"/><ellipse cx="18" cy="30" rx="12" ry="15"/><ellipse cx="45" cy="14" rx="12" ry="15"/><ellipse cx="72" cy="18" rx="11" ry="14"/><ellipse cx="88" cy="42" rx="11" ry="14"/></svg>'
new_paw2 = f'<img class="env-decor paw2" style="width:90px;" src="data:image/png;base64,{b64_correndo}" alt="Skye">'
if old_paw2 in html:
    html = html.replace(old_paw2, new_paw2, 1)
    changes += 1
    print("✓ Patinha 2 do envelope virou Skye")

# 3) DIVISOR DE PATINHAS (embaixo do nome Maitê) -> 3 SKYES PEQUENAS
divider_pattern = re.compile(r'<div class="paw-divider"[^>]*>.*?</div>', re.DOTALL)
new_divider = (
    '<div class="paw-divider" aria-hidden="true" style="align-items:center;">'
    f'<img src="data:image/png;base64,{b64_correndo}" style="width:34px;opacity:0.8;">'
    f'<img src="data:image/png;base64,{b64_sentada}" style="width:44px;">'
    f'<img src="data:image/png;base64,{b64_correndo}" style="width:34px;opacity:0.8;transform:scaleX(-1);">'
    '</div>'
)
if divider_pattern.search(html):
    html = divider_pattern.sub(new_divider, html, count=1)
    changes += 1
    print("✓ Divisor de patinhas virou trio de Skyes")

# 4) RODAPÉ -> SKYE CORRENDO
footer_pattern = re.compile(r'<div class="paw-row"[^>]*>.*?</div>', re.DOTALL)
new_footer = (
    '<div class="paw-row" aria-hidden="true">'
    f'<img src="data:image/png;base64,{b64_correndo}" style="width:52px;">'
    '</div>'
)
if footer_pattern.search(html):
    html = footer_pattern.sub(new_footer, html, count=1)
    changes += 1
    print("✓ Rodapé com Skye correndo")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nTotal de alterações aplicadas: {changes}")
print("Pronto! Abra o convite_maite_4anos.html de novo pra conferir.")
