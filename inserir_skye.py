import base64, re

HTML_FILE = "convite_maite_4anos.html"

def to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

# 1) SELO DO ENVELOPE
b64_selo = to_base64("skye_voando.png")
old_seal = '<button class="seal" id="sealBtn" aria-label="Toque para abrir o convite">M</button>'
new_seal = (
    '<button class="seal" id="sealBtn" aria-label="Toque para abrir o convite">'
    f'<img src="data:image/png;base64,{b64_selo}" alt="Skye" '
    'style="width:70%;height:70%;object-fit:contain;">'
    '</button>'
)
if old_seal in html:
    html = html.replace(old_seal, new_seal)
    print("✓ Selo do envelope atualizado")
else:
    print("⚠ Não encontrei o selo (talvez já tenha sido editado antes)")

# 2) CRACHÁ REDONDO AO LADO DA FOTO
b64_badge = to_base64("skye_sentada.png")
pattern = re.compile(r'<div class="paw-badge">.*?</div>', re.DOTALL)
new_badge = (
    f'<div class="paw-badge"><img src="data:image/png;base64,{b64_badge}" '
    'alt="Skye" style="width:80%;height:80%;object-fit:contain;"></div>'
)
if pattern.search(html):
    html = pattern.sub(new_badge, html, count=1)
    print("✓ Crachá atualizado")
else:
    print("⚠ Não encontrei o crachá (talvez já tenha sido editado antes)")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Pronto! Abra o convite_maite_4anos.html no navegador pra conferir.")
