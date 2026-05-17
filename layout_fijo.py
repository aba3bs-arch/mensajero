"""Cabecera y menú fijos al hacer scroll."""

import html as html_lib

import streamlit as st

CSS_APP = """
<style>
html, body { overflow-x: hidden; }
[data-testid="stAppViewContainer"] {
    background: #d4ce98 !important;
}
#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
}
.block-container {
    max-width: 420px !important;
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
}

.cabecera-3b {
    position: fixed !important;
    top: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 420px !important;
    z-index: 1100 !important;
    margin: 0 !important;
    background: #C8102E;
    color: #fff;
    padding: 12px 14px;
    border-radius: 0 0 14px 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.22);
    box-sizing: border-box;
}
.cabecera-3b .fila {
    display: flex;
    align-items: center;
    gap: 10px;
}
.cabecera-3b h2 {
    margin: 0;
    font-size: 17px;
    font-weight: 800;
    line-height: 1.2;
}
.cabecera-3b .sesion {
    font-size: 11px;
    opacity: 0.92;
    margin-top: 2px;
}

.nav-superior-fija {
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: calc(100% - 16px) !important;
    max-width: 404px !important;
    z-index: 1090 !important;
    background: #C4B82E !important;
    padding: 8px 10px 10px !important;
    margin: 0 !important;
    border-bottom: 2px solid rgba(0,0,0,0.08) !important;
    box-sizing: border-box !important;
    border-radius: 0 0 10px 10px !important;
}
.nav-superior-fija div[data-testid="stRadio"] > div {
    display: flex !important;
    justify-content: center !important;
    gap: 14px !important;
    flex-wrap: wrap !important;
}
.nav-superior-fija div[data-testid="stRadio"] label {
    border-radius: 50% !important;
    width: 76px !important;
    height: 76px !important;
    min-width: 76px !important;
    min-height: 76px !important;
    padding: 6px !important;
    margin: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    line-height: 1.15 !important;
}
.nav-superior-fija div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

.btn-logout-fija {
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: calc(100% - 16px) !important;
    max-width: 404px !important;
    z-index: 1089 !important;
    background: #C4B82E !important;
    padding: 0 10px 8px !important;
    margin: 0 !important;
    box-sizing: border-box !important;
}
.btn-logout-fija .stButton > button {
    width: 100% !important;
}

#espaciador-top-fijo {
    width: 100%;
    display: block;
}

/* Botones rojos solo en la app logueada, no en la pantalla PIN */
body:has(.cabecera-3b) .stButton > button {
    background: #C8102E !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 44px !important;
    font-weight: 600 !important;
}
body:has(.cabecera-3b) .stButton > button[kind="primary"] {
    background: #1E5AA8 !important;
}

div[data-testid="stForm"] {
    background: #e8e4d0;
    border-radius: 16px;
    padding: 8px 10px !important;
    border: 1px solid rgba(0,0,0,0.08);
    margin-top: 8px;
}
div[data-testid="stForm"] input {
    border-radius: 10px !important;
}
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {
    background: #1E5AA8 !important;
    color: #fff !important;
    border-radius: 50% !important;
    min-width: 44px !important;
    min-height: 44px !important;
    border: none !important;
}

#pin-top-fija {
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    width: 100% !important;
    max-width: 420px !important;
    margin: 0 auto !important;
    background: #d4ce98;
    box-sizing: border-box;
}
#espaciador-pin-top { display: none !important; height: 0 !important; }
.pin-teclado-scroll {
    max-width: 420px;
    margin: 0 auto;
    padding: 8px 8px 32px;
    position: relative;
    z-index: 101;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) {
    background: #1c1c1e !important;
    border: 3px solid #444 !important;
    border-radius: 14px !important;
    padding: 12px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .stButton > button {
    min-height: 72px !important;
    font-size: 28px !important;
    font-family: Consolas, 'Courier New', monospace !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
    background: linear-gradient(180deg, #62626a 0%, #404048 50%, #32323a 100%) !important;
    color: #fff !important;
    box-shadow: 0 5px 0 #18181c, inset 0 1px 0 rgba(255,255,255,0.18) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .stButton > button:active {
    transform: translateY(4px) !important;
    box-shadow: 0 1px 0 #18181c !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .stButton > button[kind="primary"] {
    background: linear-gradient(180deg, #3d8fd9 0%, #1E5AA8 55%, #144f94 100%) !important;
    box-shadow: 0 5px 0 #0c3560 !important;
    font-size: 16px !important;
    letter-spacing: 1px;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .pin-btn-del .stButton > button {
    background: linear-gradient(180deg, #d9534f 0%, #a52e2a 55%, #7a221f 100%) !important;
    box-shadow: 0 5px 0 #4a1513 !important;
    font-size: 15px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .stButton > button[kind="secondary"] {
    font-size: 14px !important;
    min-height: 48px !important;
}
#pin-top-fija .pin-header-rojo {
    text-align: center;
    background: #C8102E;
    color: #fff;
    padding: 18px 16px 12px;
    border-radius: 0 0 12px 12px;
}
#pin-top-fija .pin-header-rojo h2 {
    margin: 8px 0 4px;
    font-size: 20px;
}
#pin-top-fija .pin-header-rojo p {
    margin: 0;
    opacity: 0.9;
    font-size: 13px;
}
</style>
<script>
(function() {
    function altura(el) { return el ? el.offsetHeight : 0; }

    function fijarSuperior() {
        var cab = document.querySelector('.cabecera-3b');
        var esp = document.getElementById('espaciador-top-fijo');
        if (!cab || !esp) return;

        var cabH = altura(cab);
        var radio = null;
        var radios = document.querySelectorAll('[data-testid="stRadio"]');
        for (var i = 0; i < radios.length; i++) {
            if (cab.compareDocumentPosition(radios[i]) & Node.DOCUMENT_POSITION_FOLLOWING) {
                radio = radios[i];
                break;
            }
        }

        var navH = 0;
        if (radio) {
            var navWrap = radio.closest('[data-testid="stVerticalBlock"]') || radio.parentElement;
            if (navWrap) {
                navWrap.classList.add('nav-superior-fija');
                navWrap.style.top = cabH + 'px';
                navH = altura(navWrap);
            }
        }

        var logH = 0;
        var btns = document.querySelectorAll('.stButton > button');
        for (var j = 0; j < btns.length; j++) {
            var t = (btns[j].textContent || '').trim();
            if (t.indexOf('Cerrar') >= 0 || t.indexOf('🔓') >= 0) {
                var logWrap = btns[j].closest('[data-testid="stVerticalBlock"]') || btns[j].parentElement;
                if (logWrap && cab.compareDocumentPosition(logWrap) & Node.DOCUMENT_POSITION_FOLLOWING) {
                    logWrap.classList.add('btn-logout-fija');
                    logWrap.style.top = (cabH + navH) + 'px';
                    logH = altura(logWrap);
                    break;
                }
            }
        }

        esp.style.height = (cabH + navH + logH + 6) + 'px';
    }

    function aplicar() {
        if (document.querySelector('.cabecera-3b')) fijarSuperior();
    }
    aplicar();
    window.addEventListener('resize', aplicar);
    setTimeout(aplicar, 300);
    setTimeout(aplicar, 900);
})();
</script>
"""


def inyectar_estilos_app():
    st.markdown(CSS_APP, unsafe_allow_html=True)


def render_cabecera(usuario, logo_html):
    nombre = html_lib.escape(str(usuario.get("nombre", "")))
    puesto = html_lib.escape(str(usuario.get("puesto", "Tienda")))
    st.markdown(
        f"""
        <div class="cabecera-3b">
            <div class="fila">
                {logo_html}
                <div>
                    <h2>3B OFFICIAL</h2>
                    <div class="sesion">🔒 {nombre} · {puesto}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def abrir_barra_nav():
    pass


def cerrar_barra_nav():
    pass


def espaciador_contenido():
    st.markdown('<div id="espaciador-top-fijo"></div>', unsafe_allow_html=True)


inyectar_css_layout_fijo = inyectar_estilos_app
render_cabecera_fija = render_cabecera
abrir_bloque_nav = abrir_barra_nav
cerrar_bloque_nav = cerrar_barra_nav
