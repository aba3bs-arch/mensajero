"""
Genera secrets para Streamlit Cloud y para desarrollo local.

Uso:
  python generar_secrets_cloud.py

Crea:
  - .streamlit/secrets.toml  (local, no subir a GitHub)
  - secrets_para_nube.toml   (copiar y pegar en share.streamlit.io → Secrets)
"""

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
USUARIOS = RAIZ / "usuarios_pin.json"
SALIDA_LOCAL = RAIZ / ".streamlit" / "secrets.toml"
SALIDA_NUBE = RAIZ / "secrets_para_nube.toml"

SUPABASE_URL = "https://yckvxerrxgeqxzqtepdk.supabase.co"
SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlja3Z4ZXJyeGdlcXh6cXRlcGRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg4OTU4OTcsImV4cCI6MjA5NDQ3MTg5N30."
    "vNcyZ7NIGkh3GH7JUyz1S8RQh5JBO-c_AKiU_rj5LJQ"
)


def main():
    if not USUARIOS.is_file():
        print(f"No existe {USUARIOS}")
        return 1

    usuarios_json = USUARIOS.read_text(encoding="utf-8").strip()
    json.loads(usuarios_json)

    contenido = f'''# Generado automáticamente — no subas este archivo a GitHub público

[supabase]
url = "{SUPABASE_URL}"
key = "{SUPABASE_KEY}"

usuarios_pin_json = \'\'\'
{usuarios_json}
\'\'\'
'''

    SALIDA_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    SALIDA_LOCAL.write_text(contenido, encoding="utf-8")
    SALIDA_NUBE.write_text(contenido, encoding="utf-8")

    print()
    print("=" * 60)
    print("  Listo para Streamlit Cloud")
    print("=" * 60)
    print()
    print(f"  Local:  {SALIDA_LOCAL}")
    print(f"  Nube:   {SALIDA_NUBE}")
    print()
    print("  Mañana en https://share.streamlit.io :")
    print("  1. Tu app -> Settings -> Secrets")
    print("  2. Pega TODO el contenido de secrets_para_nube.toml")
    print("  3. Save → Reboot app")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
