"""Pantalla de acceso — teclado ATM (componente HTML, funciona en móvil)."""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

_TECLADO = components.declare_component(
    "teclado_pin_3b",
    path=str(Path(__file__).resolve().parent / "teclado_pin"),
)

PIN_CSS = """
<style>
html.pin-page [data-testid="stAppViewContainer"] {
    background: #b0b0b0 !important;
}
html.pin-page .block-container {
    max-width: 440px !important;
    margin: 0 auto !important;
    padding: 12px 10px 20px !important;
}
.pin-brand {
    text-align: center;
    font-family: 'Segoe UI', system-ui, sans-serif;
    margin-bottom: 8px;
    color: #222;
}
.pin-brand h1 {
    margin: 8px 0 0;
    font-size: 22px;
    font-weight: 800;
    color: #C8102E;
}
.pin-brand p {
    margin: 4px 0 0;
    font-size: 12px;
    color: #444;
    font-weight: 600;
}
html.pin-page [data-testid="stAlert"] {
    max-width: 400px;
    margin: 0 auto 8px !important;
}
html.pin-page footer,
html.pin-page [data-testid="stToolbar"],
html.pin-page .stAppDeployButton,
html.pin-page [data-testid="stDecoration"],
html.pin-page [data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
}
</style>
<script>document.documentElement.classList.add('pin-page');</script>
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
            <h1>3B OFFICIAL</h1>
            <p>ABARROTES LAS 3B · ACCESO EMPLEADOS</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.pin_error:
        st.error(st.session_state.pin_error)

    resultado = _TECLADO(
        pin_length=pin_longitud,
        value=st.session_state.pin_buffer,
        key="teclado_pin_atm",
        default="",
        height=420,
    )

    if resultado is not None and resultado != st.session_state.get("_pin_sync"):
        st.session_state._pin_sync = resultado
        if isinstance(resultado, str) and resultado.startswith("__enter__:"):
            st.session_state.pin_buffer = resultado.split(":", 1)[1]
            pin = st.session_state.pin_buffer
            if len(pin) != pin_longitud:
                st.session_state.pin_error = f"El PIN debe tener {pin_longitud} dígitos."
            else:
                usuario = buscar_usuario_por_pin(pin, usuarios)
                if usuario:
                    st.session_state.autenticado = True
                    st.session_state.usuario = usuario
                    st.session_state.vista = "chat"
                    st.session_state.chat_destino_id = None
                    st.session_state.pin_buffer = ""
                    st.session_state.pin_error = ""
                    st.rerun()
                else:
                    st.session_state.pin_error = "PIN incorrecto o usuario inactivo."
                    st.session_state.pin_buffer = ""
        elif isinstance(resultado, str):
            st.session_state.pin_buffer = resultado
            st.session_state.pin_error = ""
            if len(st.session_state.pin_buffer) == pin_longitud:
                usuario = buscar_usuario_por_pin(st.session_state.pin_buffer, usuarios)
                if usuario:
                    st.session_state.autenticado = True
                    st.session_state.usuario = usuario
                    st.session_state.vista = "chat"
                    st.session_state.chat_destino_id = None
                    st.session_state.pin_buffer = ""
                    st.session_state.pin_error = ""
                    st.rerun()
                else:
                    st.session_state.pin_error = "PIN incorrecto o usuario inactivo."
                    st.session_state.pin_buffer = ""
        st.rerun()
