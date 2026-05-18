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
    background:
        linear-gradient(180deg, rgba(255, 248, 235, 0.88) 0%, rgba(255, 245, 220, 0.92) 100%),
        url('/static/bg_tienda_3b.png') center center / cover no-repeat fixed !important;
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

/* ── Cabecera estilo WhatsApp / 3B ── */
.cabecera-3b {
    position: fixed !important;
    top: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 440px !important;
    z-index: 1100 !important;
    margin: 0 !important;
    background: linear-gradient(180deg, #B80E28 0%, #8B0A1E 100%) !important;
    color: #fff;
    padding: 10px 14px 8px;
    border-radius: 0 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    box-sizing: border-box;
}
.cabecera-3b .wa-header-top {
    display: flex;
    align-items: center;
    gap: 10px;
}
.cabecera-3b .wa-logo {
    flex-shrink: 0;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: #F5D000;
    border: 2px solid #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}
.cabecera-3b .wa-logo img, .cabecera-3b .wa-logo svg {
    max-height: 36px;
    width: auto;
}
.cabecera-3b .wa-titles { flex: 1; min-width: 0; }
.cabecera-3b h2 {
    margin: 0;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.06em;
    line-height: 1.2;
    text-transform: uppercase;
}
.cabecera-3b .sesion {
    font-size: 11px;
    opacity: 0.9;
    margin-top: 2px;
    font-weight: 500;
}
.cabecera-3b .wa-header-icons {
    display: flex;
    gap: 14px;
    font-size: 18px;
    opacity: 0.95;
    flex-shrink: 0;
}
.cabecera-3b .badge-puesto {
    display: none;
}

/* ── Pestañas CHATS / PERSONAL (barra roja) ── */
.nav-superior-fija {
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 440px !important;
    z-index: 1090 !important;
    background: linear-gradient(180deg, #8B0A1E 0%, #7A0918 100%) !important;
    padding: 0 8px 6px !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15) !important;
    box-sizing: border-box !important;
    border-radius: 0 !important;
}
.nav-superior-fija div[data-testid="stRadio"] > div {
    display: flex !important;
    justify-content: stretch !important;
    gap: 0 !important;
    background: transparent !important;
    border-radius: 0 !important;
    padding: 0 !important;
    border-bottom: 1px solid rgba(255,255,255,0.15);
}
.nav-superior-fija div[data-testid="stRadio"] label {
    flex: 1 !important;
    border-radius: 0 !important;
    width: auto !important;
    height: 40px !important;
    min-height: 40px !important;
    min-width: 0 !important;
    padding: 0 8px !important;
    margin: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    color: rgba(255,255,255,0.65) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    text-transform: uppercase !important;
    transition: all 0.15s ease !important;
}
.nav-superior-fija div[data-testid="stRadio"] label[data-checked="true"],
.nav-superior-fija div[data-testid="stRadio"] label:has(input:checked) {
    background: transparent !important;
    color: #fff !important;
    border-bottom-color: #F5D000 !important;
    box-shadow: none !important;
}
.nav-superior-fija div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

.btn-logout-fija {
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 440px !important;
    z-index: 1089 !important;
    background: rgba(139, 10, 30, 0.95) !important;
    padding: 4px 12px 8px !important;
    margin: 0 !important;
    box-sizing: border-box !important;
}
.btn-logout-fija .stButton > button {
    width: 100% !important;
    background: rgba(255,255,255,0.12) !important;
    color: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    min-height: 36px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
.btn-logout-fija .stButton > button:hover {
    border-color: #F5D000 !important;
    color: #fff !important;
    background: rgba(255,255,255,0.2) !important;
}

#espaciador-top-fijo { width: 100%; display: block; }

/* ── Modo conversación activa (una sola cabecera, chat a pantalla completa) ── */
html.modo-chat-activo [data-testid="stAppViewContainer"] {
    background: #C5B358 !important;
}
html.modo-chat-activo .nav-superior-fija,
html.modo-chat-activo .btn-logout-fija {
    display: none !important;
    height: 0 !important;
    visibility: hidden !important;
}
html.modo-chat-activo [data-testid="stCaptionContainer"],
html.modo-chat-activo .st-key-volver_conversaciones {
    display: none !important;
}
html.modo-chat-activo .cabecera-3b .wa-header-icons {
    display: none !important;
}
html.modo-chat-activo .st-key-volver_header {
    position: fixed !important;
    top: calc(8px + env(safe-area-inset-top, 0px)) !important;
    left: 6px !important;
    z-index: 1201 !important;
    width: 48px !important;
    max-width: 48px !important;
}
html.modo-chat-activo .st-key-volver_header .stButton > button {
    background: transparent !important;
    color: #fff !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 26px !important;
    min-height: 42px !important;
    padding: 0 !important;
    width: 48px !important;
}
html.modo-chat-activo .cabecera-en-chat .wa-titles {
    padding-left: 40px;
}
html.modo-chat-activo .cabecera-en-chat h2 {
    font-size: 16px !important;
    letter-spacing: 0.03em !important;
}
html.modo-chat-activo .block-container {
    padding-left: 0 !important;
    padding-right: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}
html.modo-chat-activo iframe[data-testid="stIFrame"] {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    border: none !important;
    border-radius: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}
html.modo-chat-activo div[data-testid="stForm"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 440px !important;
    z-index: 1050 !important;
    margin: 0 !important;
    border-radius: 24px 24px 0 0 !important;
    padding: 10px 12px calc(10px + env(safe-area-inset-bottom, 0px)) !important;
}
html.modo-chat-activo div:has(.zona-chat-marker) + div iframe,
html.modo-chat-activo div:has(.zona-chat-marker) ~ div iframe {
    min-height: 200px;
}
html.modo-chat-activo [data-testid="stFileUploader"] label {
    font-size: 0 !important;
}
html.modo-chat-activo [data-testid="stFileUploader"] label::after {
    content: '📷 Foto';
    font-size: 12px;
    color: #666;
}

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
    font-size: 14px;
    font-weight: 700;
    color: #8B0A1E;
    margin: 0;
    padding: 12px 14px 4px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.lista-chats-sub {
    font-size: 12px;
    color: #666;
    margin: 0;
    padding: 0 14px 10px;
    line-height: 1.4;
    border-bottom: 1px solid #eee;
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
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 14px 14px 14px 72px !important;
    min-height: 68px !important;
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 1px solid #ece5d8 !important;
    background: #fff !important;
    color: #111 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    position: relative !important;
    white-space: pre-line !important;
}
div:has(.lista-chats-marker) ~ [data-testid="stVerticalBlock"] .stButton > button::before {
    content: '3B';
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(145deg, #F5D000, #e6c200);
    border: 2px solid #C8102E;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 900;
    color: #111;
}
div:has(.lista-chats-marker) ~ [data-testid="stVerticalBlock"] .stButton > button[kind="primary"] {
    background: #fff8e8 !important;
}

/* ── Formulario envío chat ── */
div[data-testid="stForm"] {
    background: #fff !important;
    border-radius: 28px !important;
    padding: 8px 10px !important;
    border: 1px solid #ddd !important;
    margin-top: 8px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.1) !important;
}
div[data-testid="stForm"] input,
div[data-testid="stForm"] textarea {
    border-radius: 20px !important;
    border: none !important;
    background: #f5f5f5 !important;
    font-size: 15px !important;
    padding: 12px 14px !important;
}
div[data-testid="stForm"] [data-testid="stFileUploader"] {
    margin-bottom: 8px;
}
div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
    background: #1E5AA8 !important;
    color: #fff !important;
    border-radius: 50% !important;
    min-width: 52px !important;
    min-height: 52px !important;
    width: 52px !important;
    height: 52px !important;
    border: none !important;
    font-size: 20px !important;
    box-shadow: 0 4px 12px rgba(30,90,168,0.4) !important;
    padding: 0 !important;
}

.wa-lista-panel {
    background: #fff;
    border-radius: 12px 12px 0 0;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    margin: 0;
}
html:not(.modo-chat-activo) div:has(.lista-chats-marker) ~ [data-testid="stVerticalBlock"] {
    background: #fff;
    max-width: 440px;
    margin: 0 auto;
    border-radius: 0 0 12px 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    padding-bottom: 8px;
}
body:has(.cabecera-3b) iframe[data-testid="stIFrame"] {
    border-radius: 0 !important;
    border: none !important;
    box-shadow: none !important;
}
/* ── Admin ── */
div:has(.admin-panel-marker) {
    background: #fff;
    border-radius: 14px;
    padding: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    margin-top: 8px;
}
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
        max-width: 100% !important;
        width: 100% !important;
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
        var enChat = document.documentElement.classList.contains('modo-chat-activo');
        if (!enChat && !esMovil()) return;
        var esp = document.getElementById('espaciador-top-fijo');
        var espH = esp ? esp.offsetHeight : 0;
        var vh = window.innerHeight;
        var form = document.querySelector('div[data-testid="stForm"]');
        var formH = form ? form.offsetHeight : (enChat ? 72 : 160);
        var objetivo = Math.max(200, vh - espH - formH - (enChat ? 8 : 100));
        document.querySelectorAll('iframe[data-testid="stIFrame"]').forEach(function(fr) {
            fr.style.height = objetivo + 'px';
            fr.style.minHeight = objetivo + 'px';
        });
    }

    function fijarSuperior() {
        var cab = document.querySelector('.cabecera-3b');
        var esp = document.getElementById('espaciador-top-fijo');
        if (!cab || !esp) return;

        var cabH = altura(cab);
        if (document.documentElement.classList.contains('modo-chat-activo')) {
            esp.style.height = (cabH + 6) + 'px';
            ajustarIframeChat();
            return;
        }
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


def render_cabecera(usuario, logo_html, titulo_chat=None, subtitulo_chat=None):
    nombre = html_lib.escape(str(usuario.get("nombre", "")))
    if titulo_chat:
        titulo_h = html_lib.escape(str(titulo_chat))
        linea2 = html_lib.escape(str(subtitulo_chat or ""))
        clase_extra = " cabecera-en-chat"
    else:
        titulo_h = "3B MENSAJERÍA OFICIAL"
        linea2 = nombre
        clase_extra = ""
    st.markdown(
        f"""
        <div class="cabecera-3b{clase_extra}">
            <div class="wa-header-top">
                <div class="wa-logo">{logo_html}</div>
                <div class="wa-titles">
                    <h2>{titulo_h}</h2>
                    <div class="sesion">{linea2}</div>
                </div>
                <div class="wa-header-icons" aria-hidden="true">
                    <span>⚙</span><span>⋮</span>
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
