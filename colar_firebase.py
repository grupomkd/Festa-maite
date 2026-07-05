import re

FIREBASE_CONFIG = """const firebaseConfig = {
  apiKey: "AIzaSyCevP3Fqygx3-PjdR6UpUfQwnLI3BTfihs",
  authDomain: "convite-maite-4anos.firebaseapp.com",
  projectId: "convite-maite-4anos",
  storageBucket: "convite-maite-4anos.firebasestorage.app",
  messagingSenderId: "1087577366187",
  appId: "1:1087577366187:web:9c05eddca64969cafca1ee"
};"""

placeholder_pattern = re.compile(r'const firebaseConfig = \{.*?\};', re.DOTALL)

for filename in ["convite_maite_4anos.html", "admin.html"]:
    try:
        with open(filename, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠ {filename} não encontrado nesta pasta")
        continue

    if placeholder_pattern.search(content):
        content = placeholder_pattern.sub(FIREBASE_CONFIG, content, count=1)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Configuração colada em {filename}")
    else:
        print(f"⚠ Não encontrei o bloco firebaseConfig em {filename}")
