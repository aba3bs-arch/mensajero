"""Pantalla de acceso — teclado ATM con botones Streamlit (sin componente externo)."""

import streamlit as st

PIN_CSS = """
<style>
html.pin-page [data-testid="stAppViewContainer"] {
    background:
        linear-gradient(180deg, rgba(255, 248, 235, 0.9) 0%, rgba(255, 245, 220, 0.92) 100%),
        url('/static/bg_tienda_3b.png') center center / cover no-repeat fixed !important;
}
html.pin-page .block-container {
    max-width: 440px !important;
    margin: 0 auto !important;
    padding: 12px 10px 24px !important;
}
.pin-brand {
    text-align: center;
    font-family: 'Segoe UI', system-ui, sans-serif;
    margin: 0 auto 14px;
    max-width: 400px;
    background: linear-gradient(180deg, #B80E28, #8B0A1E);
    color: #fff;
    padding: 20px 16px 16px;
    border-radius: 0 0 20px 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.pin-brand h1 {
    margin: 10px 0 0;
    font-size: 18px;
    font-weight: 800;
    color: #fff;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.pin-brand p {
    margin: 6px 0 0;
    font-size: 12px;
    color: rgba(255,255,255,0.9);
    font-weight: 500;
}
.pin-lcd-wrap {
    background: linear-gradient(180deg, #1a2e1a, #0a140a);
    border: 3px solid #4a5a4a;
    border-radius: 8px;
    padding: 14px;
    margin: 0 auto 14px;
    max-width: 400px;
    text-align: center;
    box-shadow: inset 0 4px 12px rgba(0,0,0,0.5);
}
.pin-lcd-label {
    color: #6a9f6a;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: Consolas, monospace;
    margin-bottom: 8px;
}
.pin-lcd-dots {
    color: #5cff5c;
    font-size: 28px;
    letter-spacing: 14px;
    font-family: Consolas, monospace;
    text-shadow: 0 0 10px rgba(92,255,92,0.4);
}

/* Panel teclado */
html.pin-page div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #c4c4c4 !important;
    border: 4px solid #7a7a7a !important;
    border-radius: 10px !important;
    padding: 12px 10px !important;
    max-width: 400px !important;
    margin: 0 auto !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.35) !important;
}

/* GRID 4x4: filas Streamlit → celdas de una sola cuadrícula */
html.pin-page div[data-testid="stVerticalBlockBorderWrapper"] > div > [data-testid="stVerticalBlock"] > div {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 8px !important;
    width: 100% !important;
}
html.pin-page div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] {
    display: contents !important;
}
html.pin-page div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"] {
    width: auto !important;
    min-width: 0 !important;
    flex: none !important;
}

/* Teclas numéricas */
html.pin-page div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
    min-height: 52px !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    border-radius: 6px !important;
    border: 2px solid #000 !important;
    background: linear-gradient(180deg, #3d3d3d, #1a1a1a 55%, #0d0d0d) !important;
    color: #fff !important;
    box-shadow: 0 4px 0 #000 !important;
    padding: 0 !important;
    width: 100% !important;
}
html.pin-page div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:active {
    transform: translateY(3px) !important;
    box-shadow: 0 1px 0 #000 !important;
}

/* Acciones por key de Streamlit */
html.pin-page .st-key-pin_cancelar button {
    font-size: 9px !important;
    font-weight: 800 !important;
    background: linear-gradient(180deg, #e53935 0%, #e53935 6px, #2a2a2a 6px, #1a1a1a 100%) !important;
}
html.pin-page .st-key-pin_borrar button {
    font-size: 9px !important;
    font-weight: 800 !important;
    background: linear-gradient(180deg, #fbc02d 0%, #fbc02d 6px, #2a2a2a 6px, #1a1a1a 100%) !important;
}
html.pin-page .st-key-pin_entrar button {
    font-size: 9px !important;
    font-weight: 800 !important;
    background: linear-gradient(180deg, #43a047 0%, #43a047 6px, #2a2a2a 6px, #1a1a1a 100%) !important;
}
html.pin-page .st-key-pin_empty .stButton > button {
    visibility: hidden !important;
    min-height: 52px !important;
    pointer-events: none !important;
    box-shadow: none !important;
    border: none !important;
}

html.pin-page [data-testid="stAlert"] {
    max-width: 400px;
    margin: 0 auto 8px !important;
}

/* Sin menú ni marca Streamlit (también en Cloud) */
#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
.stAppDeployButton,
.stDeployButton,
.viewerBadge_container__,
div[class*="viewerBadge"],
a[href*="streamlit.io"][target="_blank"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
footer, footer * { display: none !important; }
</style>
<script>
document.documentElement.classList.add('pin-page');
(function () {
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
    ocultarMarcaStreamlit();
    if (window.MutationObserver) {
        new MutationObserver(ocultarMarcaStreamlit).observe(document.documentElement, {
            childList: true,
            subtree: true
        });
    }
})();
</script>
"""


def _html_lcd(pin_longitud, buffer):
    puntos = "".join("●" if i < len(buffer) else "○" for i in range(pin_longitud))
    return f"""
    <div class="pin-lcd-wrap">
        <div class="pin-lcd-label">Ingrese su PIN</div>
        <div class="pin-lcd-dots">{puntos}</div>
    </div>
    """


def render_pantalla_pin(config, cargar_logo, buscar_usuario_por_pin):
    pin_longitud = config["pin_longitud"]
    usuarios = config["usuarios"]

    st.markdown(PIN_CSS, unsafe_allow_html=True)

    if "pin_buffer" not in st.session_state:
        st.session_state.pin_buffer = ""
    if "pin_error" not in st.session_state:
        st.session_state.pin_error = ""

    logo = cargar_logo("48px")
    st.markdown(
        f"""
        <div class="pin-brand">
            <div style="display:block">{logo}</div>
            <h1>3B MENSAJERÍA OFICIAL</h1>
            <p>ABARROTES LAS 3B · ACCESO EMPLEADOS</p>
        </div>
        {_html_lcd(pin_longitud, st.session_state.pin_buffer)}
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.pin_error:
        st.error(st.session_state.pin_error)

    def agregar_digit(digito):
        if len(st.session_state.pin_buffer) < pin_longitud:
            st.session_state.pin_buffer += digito
            st.session_state.pin_error = ""
        if len(st.session_state.pin_buffer) == pin_longitud:
            intentar_entrar()

    def borrar_digit():
        st.session_state.pin_buffer = st.session_state.pin_buffer[:-1]
        st.session_state.pin_error = ""

    def limpiar_pin():
        st.session_state.pin_buffer = ""
        st.session_state.pin_error = ""

    def intentar_entrar():
        if len(st.session_state.pin_buffer) != pin_longitud:
            st.session_state.pin_error = f"El PIN debe tener {pin_longitud} dígitos."
            return
        usuario = buscar_usuario_por_pin(st.session_state.pin_buffer, usuarios)
        if usuario:
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.session_state.vista = "chat"
            st.session_state.chat_destino_id = None
            st.session_state.pin_buffer = ""
            st.session_state.pin_error = ""
            st.rerun()
        st.session_state.pin_error = "PIN incorrecto o usuario inactivo."
        st.session_state.pin_buffer = ""

    def tecla(col, etiqueta, key, callback=None, args=(), tipo="secondary", vacio=False):
        with col:
            if vacio:
                st.markdown('<div class="st-key-pin_empty">', unsafe_allow_html=True)
                st.button(" ", key=key, disabled=True, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.button(
                    etiqueta,
                    key=key,
                    use_container_width=True,
                    on_click=callback,
                    args=args,
                    type=tipo,
                )

    with st.container(border=True):
        r1 = st.columns(4, gap="small")
        tecla(r1[0], "1", "pin_n_1", agregar_digit, ("1",))
        tecla(r1[1], "2", "pin_n_2", agregar_digit, ("2",))
        tecla(r1[2], "3", "pin_n_3", agregar_digit, ("3",))
        tecla(r1[3], "CANCELAR", "pin_cancelar", limpiar_pin)

        r2 = st.columns(4, gap="small")
        tecla(r2[0], "4", "pin_n_4", agregar_digit, ("4",))
        tecla(r2[1], "5", "pin_n_5", agregar_digit, ("5",))
        tecla(r2[2], "6", "pin_n_6", agregar_digit, ("6",))
        tecla(r2[3], "BORRAR", "pin_borrar", borrar_digit)

        r3 = st.columns(4, gap="small")
        tecla(r3[0], "7", "pin_n_7", agregar_digit, ("7",))
        tecla(r3[1], "8", "pin_n_8", agregar_digit, ("8",))
        tecla(r3[2], "9", "pin_n_9", agregar_digit, ("9",))
        tecla(r3[3], "ENTRAR", "pin_entrar", intentar_entrar, tipo="primary")

        r4 = st.columns(4, gap="small")
        tecla(r4[0], " ", "pin_e1", vacio=True)
        tecla(r4[1], "0", "pin_n_0", agregar_digit, ("0",))
        tecla(r4[2], " ", "pin_e2", vacio=True)
        tecla(r4[3], " ", "pin_e3", vacio=True)
