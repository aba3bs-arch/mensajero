"""Teclado PIN estilo calculadora / terminal POS."""

import html as html_lib

import streamlit as st


def render_pantalla_pin(config, cargar_logo, buscar_usuario_por_pin):
    pin_longitud = config["pin_longitud"]
    usuarios = config["usuarios"]

    if "pin_buffer" not in st.session_state:
        st.session_state.pin_buffer = ""
    if "pin_error" not in st.session_state:
        st.session_state.pin_error = ""

    logo = cargar_logo("56px")
    buf = st.session_state.pin_buffer
    display = html_lib.escape(buf) if buf else "—" * pin_longitud
    puntos = "".join("●" if i < len(buf) else "○" for i in range(pin_longitud))

    st.markdown(
        f"""
        <div id="pin-top-fija">
            <div class="pin-header-rojo">
                {logo}
                <h2>3B OFFICIAL</h2>
                <p>Terminal de acceso — ingresa tu PIN</p>
            </div>
            <div class="pin-lcd" style="margin:10px 12px 12px;">
                <div class="pin-lcd-label">PIN · {pin_longitud} dígitos</div>
                <div class="pin-lcd-dots">{puntos}</div>
                <div class="pin-lcd-value">{display}</div>
            </div>
        </div>
        <div id="espaciador-pin-top"></div>
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

    st.markdown(
        """
        <style>
        .pin-lcd {
            background: linear-gradient(180deg, #0d1f0d 0%, #051005 100%);
            border: 3px solid #2a3a2a; border-radius: 10px;
            padding: 14px 16px;
            box-shadow: inset 0 2px 12px rgba(0,0,0,0.6);
            font-family: Consolas, 'Courier New', monospace;
        }
        .pin-lcd-label { color: #5a8f5a; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; }
        .pin-lcd-dots {
            color: #39ff14; font-size: 28px; letter-spacing: 14px; text-align: center;
            text-shadow: 0 0 10px rgba(57,255,20,0.45); min-height: 40px; line-height: 40px;
        }
        .pin-lcd-value { color: #2d5a2d; font-size: 13px; text-align: right; letter-spacing: 3px; margin-top: 4px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="pin-teclado-scroll">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<span class="pin-keypad-marker" aria-hidden="true"></span>', unsafe_allow_html=True)
        for fila in ("123", "456", "789"):
            c1, c2, c3 = st.columns(3, gap="small")
            for col, digito in zip((c1, c2, c3), fila):
                with col:
                    st.button(
                        digito,
                        key=f"pin_n_{digito}_{fila}",
                        use_container_width=True,
                        on_click=agregar_digit,
                        args=(digito,),
                    )

        c_del, c_zero, c_ok = st.columns(3, gap="small")
        with c_del:
            st.markdown('<div class="pin-btn-del">', unsafe_allow_html=True)
            st.button("BORRAR", key="pin_borrar", use_container_width=True, on_click=borrar_digit)
            st.markdown("</div>", unsafe_allow_html=True)
        with c_zero:
            st.button("0", key="pin_n_0", use_container_width=True, on_click=agregar_digit, args=("0",))
        with c_ok:
            st.button("ENTRAR", key="pin_entrar", type="primary", use_container_width=True, on_click=intentar_entrar)

        st.button("C · Limpiar todo", key="pin_limpiar", use_container_width=True, on_click=limpiar_pin)
    st.markdown("</div>", unsafe_allow_html=True)
