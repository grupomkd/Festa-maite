import re

for filename in ["convite_maite_4anos.html", "admin.html"]:
    with open(filename, encoding="utf-8") as f:
        html = f.read()

    if "TIMEOUT_HELPER_V1" not in html:
        helper = """
<script id="TIMEOUT_HELPER_V1">
window.withTimeout = function(promise, ms, label){
  return Promise.race([
    promise,
    new Promise(function(_, reject){
      setTimeout(function(){
        reject(new Error('Tempo esgotado (' + (label || 'operacao') + '). Provavel bloqueio de rede/extensao (ex: AdBlock) ou Firestore nao configurado.'));
      }, ms);
    })
  ]);
};
</script>
</head>"""
        html = html.replace("</head>", helper, 1)

        # Envolve o addDoc do convite com timeout
        html = html.replace(
            "await addDoc(collection(db, 'rsvps_maite4anos'), {",
            "await withTimeout(addDoc(collection(db, 'rsvps_maite4anos'), {",
        )
        html = html.replace(
            "confirmadoEm: serverTimestamp()\n      });",
            "confirmadoEm: serverTimestamp()\n      }), 10000, 'salvar confirmacao');"
        )

        # Envolve o getDocs do admin com timeout
        html = html.replace(
            "const snap = await getDocs(q);",
            "const snap = await withTimeout(getDocs(q), 10000, 'carregar confirmacoes');"
        )

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Timeout adicionado em {filename}")
    else:
        print(f"⚠ {filename} já tem o timeout")
