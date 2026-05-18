import re
from pathlib import Path

p = Path(__file__).parent / "static" / "app_mensajero.js"
t = p.read_text(encoding="utf-8")
t = t.replace("<motion class=", "<div class=")
t = t.replace("</motion>", "</div>")
p.write_text(t, encoding="utf-8")
print("fixed")
