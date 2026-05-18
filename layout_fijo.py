"""Cabecera, menú fijos y estilos globales de la app."""

import html as html_lib

import streamlit as st

CSS_APP = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body {
    overflow-x: hidden;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(165deg, #f8f6f0 0%, #ebe8dc 45%, #e2dcc8 100%) !important;
}
#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stToolbarActions"],
.stAppDeployButton,
.stDeployButton,
.viewerBadge_container__,
div[class*="viewerBadge"],
a[data-testid="stHeaderActionElements"],
a[href*="streamlit.io"][target="_blank"] {
    visibility: hidden !important;
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
footer, footer * {
    display: none !important;
    visibility: hidden !important;
}
.block-container {
    max-width: 440px !important;
    padding-top: 0 !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
    padding-bottom: 2.5rem !important;
}

/* ── Cabecera ── */
.cabecera-3b {
    position: fixed !important;
    top: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 440px !important;
    z-index: 1100 !important;
    margin: 0 !important;
    background: linear-gradient(135deg, #C8102E 0%, #9B0C24 100%);
    color: #fff;
    padding: 14px 16px 12px;
    border-radius: 0 0 18px 18px;
    box-shadow: 0 6px 24px rgba(155, 12, 36, 0.35);
    box-sizing: border-box;
}
.cabecera-3b .fila {
    display: flex;
    align-items: center;
    gap: 12px;
}
.cabecera-3b h2 {
    margin: 0;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.02em;
    line-height: 1.2;
}
.cabecera-3b .sesion {
    font-size: 12px;
    opacity: 0.92;
    margin-top: 3px;
    font-weight: 500;
}
.cabecera-3b .badge-puesto {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 11px;
    margin-top: 4px;
}

/* ── Navegación (pestañas) ── */
.nav-superior-fija {
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: calc(100% - 24px) !important;
    max-width: 416px !important;
    z-index: 1090 !important;
    background: #fff !important;
    padding: 10px 12px !important;
    margin: 0 !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important;
    box-sizing: border-box !important;
    border-radius: 14px !important;
}
.nav-superior-fija div[data-testid="stRadio"] > div {
    display: flex !important;
    justify-content: stretch !important;
    gap: 8px !important;
    background: #f0ede4 !important;
    border-radius: 12px !important;
    padding: 4px !important;
}
.nav-superior-fija div[data-testid="stRadio"] label {
    flex: 1 !important;
    border-radius: 10px !important;
    width: auto !important;
    height: 42px !important;
    min-height: 42px !important;
    min-width: 0 !important;
    padding: 0 12px !important;
    margin: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #555 !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.15s ease !important;
}
.nav-superior-fija div[data-testid="stRadio"] label[data-checked="true"],
.nav-superior-fija div[data-testid="stRadio"] label:has(input:checked) {
    background: #fff !important;
    color: #C8102E !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}
.nav-superior-fija div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

.btn-logout-fija {
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: calc(100% - 24px) !important;
    max-width: 416px !important;
    z-index: 1089 !important;
    background: transparent !important;
    padding: 4px 0 8px !important;
    margin: 0 !important;
    box-sizing: border-box !important;
}
.btn-logout-fija .stButton > button {
    width: 100% !important;
    background: transparent !important;
    color: #666 !important;
    border: 1px dashed #ccc !important;
    min-height: 38px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.btn-logout-fija .stButton > button:hover {
    border-color: #C8102E !important;
    color: #C8102E !important;
    background: #fff5f5 !important;
}

#espaciador-top-fijo { width: 100%; display: block; }

/* ── Botones generales (app logueada) ── */
body:has(.cabecera-3b) .stButton > button {
    background: #fff !important;
    color: #1a1a1a !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
    transition: transform 0.1s, box-shadow 0.15s !important;
}
body:has(.cabecera-3b) .stButton > button:hover {
    border-color: #C8102E !important;
    box-shadow: 0 4px 12px rgba(200,16,46,0.12) !important;
}
body:has(.cabecera-3b) .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #C8102E, #9B0C24) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(200,16,46,0.3) !important;
}
body:has(.cabecera-3b) .stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 18px rgba(200,16,46,0.4) !important;
}

/* ── Lista de conversaciones ── */
.lista-chats-titulo {
    font-size: 22px;
    font-weight: 800;
    color: #1a1a1a;
    margin: 8px 0 4px;
    letter-spacing: -0.02em;
}
.lista-chats-sub {
    font-size: 13px;
    color: #666;
    margin-bottom: 16px;
    line-height: 1.45;
}
div[data-testid="stVerticalBlock"]:has(.lista-chats-marker) h3 {
    display: none !important;
}
div[data-testid="stVerticalBlock"]:has(.lista-chats-marker) .stButton > button[kind="primary"],
div[data-testid="stVerticalBlock"]:has(.lista-chats-marker) ~ div .stButton > button {
    text-align: left !important;
    padding-left: 16px !important;
}
div:has(.lista-chats-marker) ~ [data-testid="stVerticalBlock"] .stButton > button {
    justify-content: flex-start !important;
}

/* ── Formulario envío chat ── */
div[data-testid="stForm"] {
    background: #fff;
    border-radius: 16px;
    padding: 12px 14px !important;
    border: 1px solid rgba(0,0,0,0.08);
    margin-top: 12px;
    box-shadow: 0 -4px 24px rgba(0,0,0,0.06);
}
div[data-testid="stForm"] input,
div[data-testid="stForm"] textarea {
    border-radius: 12px !important;
    border: 1px solid #e0ddd4 !important;
    font-size: 15px !important;
}
div[data-testid="stForm"] [data-testid="stFileUploader"] {
    margin-bottom: 8px;
}
div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #1E5AA8, #144f94) !important;
    color: #fff !important;
    border-radius: 12px !important;
    min-width: 48px !important;
    min-height: 48px !important;
    border: none !important;
    font-size: 18px !important;
    box-shadow: 0 4px 12px rgba(30,90,168,0.35) !important;
}

/* ── Admin ── */
div:has(.admin-panel-marker) [data-testid="stExpander"] {
    background: #fff;
    border-radius: 12px;
    border: 1px solid rgba(0,0,0,0.06);
}
div:has(.admin-panel-marker) h3 {
    font-weight: 800 !important;
}

/* ── Alertas ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}
.stCaption, [data-testid="stCaptionContainer"] {
    color: #777 !important;
    font-size: 12px !important;
}

/* ── PIN ── */
#pin-top-fija {
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    width: 100% !important;
    max-width: 440px !important;
    margin: 0 auto !important;
    box-sizing: border-box;
}
#espaciador-pin-top { display: none !important; height: 0 !important; }
body:not(:has(.cabecera-3b)) [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f5f3eb 0%, #e8e4d6 100%) !important;
}
.pin-teclado-scroll {
    max-width: 440px;
    margin: 0 auto;
    padding: 8px 4px 32px;
    position: relative;
    z-index: 101;
}
#pin-top-fija .pin-header-rojo {
    text-align: center;
    background: linear-gradient(135deg, #C8102E 0%, #9B0C24 100%);
    color: #fff;
    padding: 24px 20px 18px;
    border-radius: 0 0 20px 20px;
    box-shadow: 0 8px 28px rgba(155, 12, 36, 0.3);
}
#pin-top-fija .pin-header-rojo h2 {
    margin: 10px 0 6px;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.04em;
}
#pin-top-fija .pin-header-rojo p {
    margin: 0;
    opacity: 0.9;
    font-size: 13px;
    font-weight: 500;
}
.pin-lcd {
    background: linear-gradient(180deg, #1a2e1a 0%, #0d180d 100%);
    border: none;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: inset 0 2px 16px rgba(0,0,0,0.5), 0 4px 12px rgba(0,0,0,0.15);
    margin: 14px 12px 16px !important;
    font-family: 'Consolas', 'Courier New', monospace;
}
.pin-lcd-label {
    color: #6a9f6a;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 600;
}
.pin-lcd-dots {
    color: #5cff5c;
    font-size: 32px;
    letter-spacing: 16px;
    text-align: center;
    text-shadow: 0 0 20px rgba(92,255,92,0.35);
    min-height: 44px;
    line-height: 44px;
    margin: 8px 0;
}
.pin-lcd-value { display: none !important; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) {
    background: #fff !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 20px !important;
    padding: 16px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .stButton > button {
    min-height: 64px !important;
    font-size: 26px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    border: 1px solid #e8e5dc !important;
    background: #faf9f6 !important;
    color: #1a1a1a !important;
    box-shadow: 0 2px 0 #e0ddd4 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .stButton > button:active {
    transform: translateY(2px) !important;
    box-shadow: none !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1E5AA8, #144f94) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(30,90,168,0.35) !important;
    font-size: 15px !important;
    letter-spacing: 0.5px;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .pin-btn-del .stButton > button {
    background: #fff5f5 !important;
    color: #C8102E !important;
    border-color: #f0c0c0 !important;
    font-size: 13px !important;
    min-height: 64px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.pin-keypad-marker) .stButton > button[kind="secondary"] {
    font-size: 13px !important;
    min-height: 44px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #888 !important;
}

@media (max-width: 480px) {
    .block-container {
        max-width: 100% !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        padding-bottom: calc(16px + env(safe-area-inset-bottom, 0px)) !important;
    }
    [data-testid="stAppViewContainer"] {
        padding-top: env(safe-area-inset-top, 0px);
    }
    .cabecera-3b {
        max-width: 100% !important;
        padding-top: calc(12px + env(safe-area-inset-top, 0px)) !important;
    }
    .nav-superior-fija, .btn-logout-fija {
        max-width: calc(100% - 20px) !important;
        width: calc(100% - 20px) !important;
    }
    body:has(.cabecera-3b) .stButton > button {
        min-height: 50px !important;
    }
    div[data-testid="stForm"] {
        position: sticky !important;
        bottom: 0 !important;
        z-index: 1050 !important;
        margin-bottom: env(safe-area-inset-bottom, 8px) !important;
        box-shadow: 0 -8px 28px rgba(0,0,0,0.12) !important;
    }
    div[data-testid="stForm"] input {
        font-size: 16px !important;
        min-height: 48px !important;
    }
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
        min-width: 52px !important;
        min-height: 52px !important;
    }
    #pin-top-fija { max-width: 100% !important; }
    iframe[data-testid="stIFrame"] {
        border-radius: 12px !important;
    }
}
</style>
<script>
(function() {
    function altura(el) { return el ? el.offsetHeight : 0; }
    function esMovil() { return window.innerWidth <= 480; }

    function ajustarIframeChat() {
        if (!esMovil()) return;
        var esp = document.getElementById('espaciador-top-fijo');
        var espH = esp ? esp.offsetHeight : 0;
        var vh = window.innerHeight;
        var form = document.querySelector('div[data-testid="stForm"]');
        var formH = form ? form.offsetHeight : 160;
        var cap = document.querySelector('[data-testid="stCaptionContainer"]');
        var capH = cap ? cap.offsetHeight : 20;
        var objetivo = Math.max(240, vh - espH - formH - capH - 100);
        document.querySelectorAll('iframe[data-testid="stIFrame"]').forEach(function(fr) {
            if (fr.offsetHeight >= 180) {
                fr.style.height = objetivo + 'px';
                fr.style.minHeight = objetivo + 'px';
            }
        });
    }

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
                navWrap.style.top = (cabH + 8) + 'px';
                navH = altura(navWrap);
            }
        }

        var logH = 0;
        var btns = document.querySelectorAll('.stButton > button');
        for (var j = 0; j < btns.length; j++) {
            var t = (btns[j].textContent || '').trim();
            if (t.indexOf('Cerrar') >= 0 || t.indexOf('sesión') >= 0) {
                var logWrap = btns[j].closest('[data-testid="stVerticalBlock"]') || btns[j].parentElement;
                if (logWrap && cab.compareDocumentPosition(logWrap) & Node.DOCUMENT_POSITION_FOLLOWING) {
                    logWrap.classList.add('btn-logout-fija');
                    logWrap.style.top = (cabH + navH + 12) + 'px';
                    logH = altura(logWrap);
                    break;
                }
            }
        }

        esp.style.height = (cabH + navH + logH + 14) + 'px';
    }

    function ocultarMarcaStreamlit() {
        var rx = /hosted with streamlit|made with streamlit/i;
        document.querySelectorAll('a, button, p, span, small, footer').forEach(function (el) {
            var txt = (el.textContent || '').trim();
            if (!txt || txt.length > 120 || !rx.test(txt)) return;
            var n = el;
            for (var i = 0; i < 8 && n; i++) {
                n.style.setProperty('display', 'none', 'important');
                n.style.setProperty('visibility', 'hidden', 'important');
                n.style.setProperty('height', '0', 'important');
                n.style.setProperty('opacity', '0', 'important');
                n = n.parentElement;
            }
        });
    }

    function aplicar() {
        ocultarMarcaStreamlit();
        if (document.querySelector('.cabecera-3b')) fijarSuperior();
        ajustarIframeChat();
    }
    aplicar();
    if (window.MutationObserver) {
        new MutationObserver(ocultarMarcaStreamlit).observe(document.documentElement, {
            childList: true,
            subtree: true
        });
    }
    window.addEventListener('resize', aplicar);
    window.addEventListener('orientationchange', function() {
        setTimeout(aplicar, 200);
    });
    setTimeout(aplicar, 300);
    setTimeout(aplicar, 900);
    setTimeout(ajustarIframeChat, 1200);
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
                    <div class="sesion">{nombre}</div>
                    <span class="badge-puesto">{puesto}</span>
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
