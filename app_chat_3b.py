import base64
import datetime
import html
import secrets
import shutil
import unicodedata
import uuid
from pathlib import Path

import requests
import streamlit as st

from chat_privado import (
    CHAT_GENERAL_ID,
    FOTO_EXPIRA_HORAS,
    aviso_configurar_fotos,
    aviso_configurar_supabase_privado,
    construir_mensajes_html as construir_html_chat,
    enviar_foto_temporal,
    enviar_mensaje_db,
    pantalla_lista_chats,
    resolver_chat_destino,
    supabase_soporta_fotos,
    supabase_soporta_privado,
)
from layout_fijo import (
    abrir_bloque_nav,
    cerrar_bloque_nav,
    espaciador_contenido,
    inyectar_css_layout_fijo,
    render_cabecera_fija,
)
from config_app import (
    aviso_admin_en_nube,
    cargar_config,
    guardar_config,
    headers_supabase,
    obtener_supabase,
)
from pantalla_pin import render_pantalla_pin

CHAT_AUTO_REFRESH_SEC = 5

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}

LOGO_SVG = """
<svg width="42" height="48" viewBox="0 0 90 100">
  <path d="M45 4 L82 88 L8 88 Z" fill="#F5D000" stroke="#fff" stroke-width="3"/>
  <text x="45" y="28" text-anchor="middle" font-family="Arial Black,sans-serif" font-size="9" fill="#C8102E" font-weight="bold">ABARROTES</text>
  <text x="45" y="58" text-anchor="middle" font-family="Arial Black,sans-serif" font-size="26" fill="#111" font-weight="bold">3B</text>
  <rect x="18" y="68" width="54" height="14" rx="2" fill="#1E5AA8"/>
  <text x="45" y="79" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#fff" font-weight="bold">24 HRS</text>
</svg>"""


def normalizar_nombre(texto):
    texto = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in texto if unicodedata.category(c) != "Mn").strip().lower()


def es_admin(usuario):
    return bool(usuario and usuario.get("admin"))


def usuarios_activos(usuarios):
    return [u for u in usuarios if u.get("activo", True)]


def buscar_usuario_por_pin(pin, usuarios):
    pin = str(pin).strip()
    for u in usuarios:
        if not u.get("activo", True):
            continue
        if str(u.get("pin", "")).strip() == pin:
            return u
    return None


def pin_en_uso(pin, usuarios, excluir_id=None):
    pin = str(pin).strip()
    for u in usuarios:
        if excluir_id and u.get("id") == excluir_id:
            continue
        if str(u.get("pin", "")).strip() == pin:
            return True
    return False


def validar_pin(pin, pin_longitud):
    pin = str(pin).strip()
    if not pin.isdigit():
        return "El PIN solo debe tener números."
    if len(pin) != pin_longitud:
        return f"El PIN debe tener {pin_longitud} dígitos."
    return None


def contar_admins(usuarios):
    return sum(1 for u in usuarios if u.get("admin") and u.get("activo", True))


def generar_pin(pin_longitud, usuarios):
    for _ in range(50):
        pin = "".join(secrets.choice("0123456789") for _ in range(pin_longitud))
        if not pin_en_uso(pin, usuarios):
            return pin
    return None


def cargar_logo(altura="48px"):
    carpeta = Path(__file__).resolve().parent
    for nombre in ("logo_3b.png", "logo_3b.jpg", "logo_3b.webp", "logo.png", "logo.jpg"):
        ruta = carpeta / nombre
        if ruta.is_file():
            ext = ruta.suffix.lower()
            b64 = base64.b64encode(ruta.read_bytes()).decode("ascii")
            mime = MIME.get(ext, "image/png")
            return (
                f'<img src="data:{mime};base64,{b64}" alt="Logo 3B" '
                f'style="height:{altura};width:auto;object-fit:contain;display:block">'
            )
    return LOGO_SVG


def pantalla_admin(config):
    aviso_admin_en_nube()
    pin_longitud = config["pin_longitud"]
    usuarios = config["usuarios"]

    st.markdown('<span class="admin-panel-marker" style="display:none" aria-hidden="true"></span>', unsafe_allow_html=True)
    st.markdown("### 👥 Gestión de personal")
    st.caption(
        "Alta, baja y cambio de PIN sin editar archivos. "
        "Desactiva empleados que ya no trabajan (conservan historial de mensajes)."
    )

    activos = [u for u in usuarios if u.get("activo", True)]
    inactivos = [u for u in usuarios if not u.get("activo", True)]

    st.markdown(f"**Activos:** {len(activos)} · **Inactivos:** {len(inactivos)}")

    for u in usuarios:
        estado = "🟢 Activo" if u.get("activo", True) else "⚪ Inactivo"
        rol = " · Admin" if u.get("admin") else ""
        titulo = f"{u['nombre']} — {u.get('puesto', 'Tienda')} ({estado}{rol})"

        with st.expander(titulo, expanded=False):
            with st.form(f"edit_{u['id']}"):
                nombre = st.text_input("Nombre", value=u["nombre"])
                puesto = st.text_input("Puesto", value=u.get("puesto", "Tienda"))
                pin = st.text_input(
                    "PIN",
                    value=u.get("pin", ""),
                    max_chars=pin_longitud,
                    help=f"{pin_longitud} dígitos numéricos",
                )
                hacer_admin = st.checkbox("Es administrador", value=bool(u.get("admin")))
                guardar = st.form_submit_button("💾 Guardar cambios", use_container_width=True)

                if guardar:
                    err = validar_pin(pin, pin_longitud)
                    if err:
                        st.error(err)
                    elif pin_en_uso(pin, usuarios, excluir_id=u["id"]):
                        st.error("Ese PIN ya lo usa otro empleado.")
                    elif hacer_admin is False and u.get("admin") and contar_admins(usuarios) <= 1:
                        st.error("Debe quedar al menos un administrador activo.")
                    else:
                        u["nombre"] = nombre.strip()
                        u["puesto"] = puesto.strip()
                        u["pin"] = pin.strip()
                        u["admin"] = hacer_admin
                        guardar_config(config)
                        if st.session_state.usuario.get("id") == u["id"]:
                            st.session_state.usuario = u
                        st.success("Empleado actualizado.")
                        st.rerun()

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🎲 PIN aleatorio", key=f"rnd_{u['id']}", use_container_width=True):
                    nuevo = generar_pin(pin_longitud, usuarios)
                    if nuevo:
                        u["pin"] = nuevo
                        guardar_config(config)
                        st.info(f"Nuevo PIN de {u['nombre']}: **{nuevo}** (anótalo ahora)")
                        st.rerun()
                    else:
                        st.error("No se pudo generar un PIN único.")
            with c2:
                if u.get("activo", True):
                    if st.button("⏸ Desactivar", key=f"off_{u['id']}", use_container_width=True):
                        if u.get("admin") and contar_admins(usuarios) <= 1:
                            st.error("No puedes desactivar al único administrador.")
                        else:
                            u["activo"] = False
                            guardar_config(config)
                            st.success(f"{u['nombre']} desactivado (ya no puede entrar).")
                            st.rerun()
                else:
                    if st.button("▶ Reactivar", key=f"on_{u['id']}", use_container_width=True):
                        u["activo"] = True
                        guardar_config(config)
                        st.success(f"{u['nombre']} reactivado.")
                        st.rerun()
            with c3:
                if not u.get("activo", True):
                    if st.button("🗑 Eliminar", key=f"del_{u['id']}", use_container_width=True):
                        if u.get("admin") and contar_admins(usuarios) <= 1:
                            st.error("No puedes eliminar al único administrador.")
                        else:
                            config["usuarios"] = [x for x in usuarios if x["id"] != u["id"]]
                            guardar_config(config)
                            st.success("Empleado eliminado del sistema.")
                            st.rerun()

    st.divider()
    st.markdown("#### ➕ Nuevo empleado")

    with st.form("nuevo_empleado"):
        n_nombre = st.text_input("Nombre completo")
        n_puesto = st.text_input("Puesto", value="Tienda")
        n_pin = st.text_input(f"PIN ({pin_longitud} dígitos)", max_chars=pin_longitud)
        n_admin = st.checkbox("Administrador (puede gestionar personal)")
        crear = st.form_submit_button("Agregar empleado", use_container_width=True)

        if crear:
            if not n_nombre.strip():
                st.error("Escribe el nombre.")
            else:
                err = validar_pin(n_pin, pin_longitud)
                if err:
                    st.error(err)
                elif pin_en_uso(n_pin, usuarios):
                    st.error("Ese PIN ya está en uso.")
                else:
                    config["usuarios"].append(
                        {
                            "id": uuid.uuid4().hex[:8],
                            "nombre": n_nombre.strip(),
                            "puesto": n_puesto.strip() or "Tienda",
                            "pin": n_pin.strip(),
                            "admin": n_admin,
                            "activo": True,
                        }
                    )
                    guardar_config(config)
                    st.success(f"{n_nombre.strip()} agregado correctamente.")
                    st.rerun()

    if st.button("🎲 Generar PIN y agregar después", use_container_width=True):
        pin_nuevo = generar_pin(pin_longitud, usuarios)
        if pin_nuevo:
            st.session_state.pin_sugerido = pin_nuevo
            st.info(f"PIN sugerido: **{pin_nuevo}** — cópialo en el formulario de arriba.")
        else:
            st.error("No hay PINs disponibles.")


def _html_vista_chat(html_mensajes, ribbon):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        background: #C5B358;
        height: 100%; min-height: 100%;
        display: flex; flex-direction: column; overflow: hidden;
        -webkit-text-size-adjust: 100%;
    }}
    .ribbon {{
        background: #1E5AA8; color: #F5D000; text-align: center;
        font-weight: 800; font-size: 11px; padding: 6px 12px;
        letter-spacing: 0.12em;
    }}
    .ribbon.priv {{ background: #6a1b9a; color: #fff; }}
    .chat-box {{
        flex: 1; overflow-y: auto; padding: 16px 12px;
        display: flex; flex-direction: column; gap: 8px;
        background: #C5B358;
        background-image: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(0,0,0,0.06) 0%, transparent 45%);
    }}
    .msg {{
        max-width: 85%; padding: 10px 14px 8px; font-size: 14px; line-height: 1.45;
        box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }}
    .msg .sender {{ font-size: 11px; font-weight: 700; color: #2E7D32; margin-bottom: 4px; }}
    .received {{
        background: #FFF9C4; color: #1B5E20;
        border-radius: 16px 16px 16px 4px; align-self: flex-start;
        border: 1px solid rgba(0,0,0,0.06);
    }}
    .sent {{
        background: linear-gradient(135deg, #E53935, #C8102E);
        color: #fff; border-radius: 16px 16px 4px 16px; align-self: flex-end;
    }}
    .sent .sender {{ display: none; }}
    .time {{ font-size: 10px; text-align: right; margin-top: 6px; opacity: 0.7; }}
    .sent .time {{ color: rgba(255,255,255,0.85); }}
    .msg img {{ border-radius: 10px; max-width: 100%; }}
    </style>
    </head>
    <body>
    <div class="ribbon{' priv' if 'priv' in ribbon.lower() else ''}">{html.escape(ribbon)}</div>
    <div class="chat-box" id="box">{html_mensajes}</div>
    <script>const b=document.getElementById('box');b.scrollTop=b.scrollHeight;</script>
    </body>
    </html>
    """


@st.fragment(run_every=datetime.timedelta(seconds=CHAT_AUTO_REFRESH_SEC))
def _zona_mensajes_auto(nombre, dest_privado, es_privado, ribbon):
    html_mensajes = construir_html_chat(
        SUPABASE_URL,
        HEADERS,
        nombre,
        dest_privado,
        etiqueta_privado=es_privado,
        normalizar_nombre=normalizar_nombre,
    )
    codigo = _html_vista_chat(html_mensajes, ribbon)
    st.markdown('<div class="zona-chat-marker" style="display:none"></div>', unsafe_allow_html=True)
    st.components.v1.html(codigo, height=480, scrolling=False)


def pantalla_chat(usuario, config):
    if st.session_state.get("chat_destino_id") is None:
        pantalla_lista_chats(
            usuario,
            config,
            usuarios_activos,
            normalizar_nombre,
            SUPABASE_URL,
            HEADERS,
        )
        return

    dest_privado, titulo_chat, subtitulo_chat, es_privado = resolver_chat_destino(
        config, st.session_state.chat_destino_id
    )
    if titulo_chat == "Chat" and st.session_state.chat_destino_id != CHAT_GENERAL_ID:
        st.session_state.chat_destino_id = None
        st.rerun()

    nombre = usuario["nombre"]
    puesto = usuario.get("puesto", "Tienda")
    ribbon = "CHAT PRIVADO" if es_privado else "24 HRS · CHAT GENERAL"

    if es_privado and not supabase_soporta_privado(SUPABASE_URL, HEADERS):
        aviso_configurar_supabase_privado()

    if st.session_state.get("_supabase_fotos_ok") is not True:
        st.session_state.pop("_supabase_fotos_ok", None)
    fotos_ok = supabase_soporta_fotos(SUPABASE_URL, HEADERS)
    if not fotos_ok:
        aviso_configurar_fotos()

    _zona_mensajes_auto(nombre, dest_privado, es_privado, ribbon)

    with st.form("envio", clear_on_submit=True):
        foto = None
        if fotos_ok:
            foto = st.file_uploader(
                "Foto temporal",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed",
                key="foto_chat",
            )
        col_in, col_btn = st.columns([5, 1])
        with col_in:
            texto = st.text_input("Mensaje", label_visibility="collapsed", placeholder="Mensaje")
        with col_btn:
            enviar = st.form_submit_button("➤", use_container_width=True, help="Enviar")

        if enviar:
            if foto is not None:
                ok, err = enviar_foto_temporal(
                    SUPABASE_URL, HEADERS, foto, nombre, dest_privado, mensaje_caption=texto or ""
                )
            elif texto:
                ok, err = enviar_mensaje_db(
                    SUPABASE_URL, HEADERS, nombre, texto, dest_privado
                )
            else:
                ok, err = False, "Escribe un mensaje o elige una foto."
            if ok:
                st.rerun()
            else:
                st.error(err)


def barra_navegacion(usuario):
    abrir_bloque_nav()

    opciones = ["CHATS"]
    if es_admin(usuario):
        opciones.append("PERSONAL")

    if "vista" not in st.session_state:
        st.session_state.vista = "chat"

    idx = 0 if st.session_state.vista == "chat" else 1
    elegida = st.radio(
        "Menú",
        opciones,
        index=min(idx, len(opciones) - 1),
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.vista = "chat" if elegida == "CHATS" else "admin"

    if st.button("Cerrar sesión", use_container_width=True, key="cerrar_sesion"):
        st.session_state.autenticado = False
        st.session_state.usuario = None
        st.session_state.pin_buffer = ""
        st.session_state.chat_destino_id = None
        st.session_state.vista = "chat"
        st.rerun()

    cerrar_bloque_nav()


def preparar_icono_pwa():
    """Copia logo_3b.png a static/ para el ícono al instalar en el celular."""
    carpeta = Path(__file__).resolve().parent
    static = carpeta / "static"
    static.mkdir(exist_ok=True)
    destino = static / "logo_3b.png"
    if destino.is_file():
        return
    for nombre in ("logo_3b.png", "logo_3b.jpg", "logo.png"):
        origen = carpeta / nombre
        if origen.is_file():
            shutil.copy(origen, destino)
            break


def inyectar_pantalla_completa():
    """PWA + meta móvil: mejor aspecto al instalar en pantalla de inicio."""
    st.markdown(
        """
        <link rel="manifest" href="/static/manifest.json">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="3B Official">
        <meta name="theme-color" content="#C8102E">
        <meta name="format-detection" content="telephone=no">
        """,
        unsafe_allow_html=True,
    )
    st.components.v1.html(
        """
        <div id="fs-bar" style="
            display:none; position:fixed; bottom:0; left:0; right:0; z-index:999999;
            background:#1E5AA8; color:#fff; text-align:center; padding:12px;
            font-family:sans-serif; font-size:14px; box-shadow:0 -2px 12px rgba(0,0,0,0.25);
        ">
            <button id="fs-btn" style="
                background:#fff; color:#1E5AA8; border:none; border-radius:24px;
                padding:12px 28px; font-size:16px; font-weight:bold; width:90%; max-width:320px;
            ">⛶ Pantalla completa</button>
        </div>
        <script>
        (function() {
            function docRoot() {
                try { return window.top.document.documentElement; } catch(e) {}
                return document.documentElement;
            }
            function esModoApp() {
                try {
                    if (window.top.matchMedia('(display-mode: standalone)').matches) return true;
                    if (window.top.navigator.standalone === true) return true;
                } catch(e) {}
                return false;
            }
            function estaFullscreen() {
                try {
                    const d = window.top.document;
                    return !!(d.fullscreenElement || d.webkitFullscreenElement);
                } catch(e) { return false; }
            }
            function entrarFullscreen() {
                const el = docRoot();
                try {
                    if (el.requestFullscreen) return el.requestFullscreen();
                    if (el.webkitRequestFullscreen) return el.webkitRequestFullscreen();
                } catch(e) {}
            }
            function esMovil() {
                return window.innerWidth <= 480;
            }
            function actualizarBarra() {
                const bar = document.getElementById('fs-bar');
                if (!bar) return;
                if (esModoApp() || estaFullscreen() || !esMovil()) {
                    bar.style.display = 'none';
                } else {
                    bar.style.display = 'block';
                }
            }
            document.getElementById('fs-btn').addEventListener('click', function() {
                entrarFullscreen().then(actualizarBarra).catch(actualizarBarra);
            });
            ['fullscreenchange','webkitfullscreenchange'].forEach(function(ev) {
                try { window.top.document.addEventListener(ev, actualizarBarra); } catch(e) {}
            });
            actualizarBarra();
        })();
        </script>
        """,
        height=70,
    )


# ── Inicio ──
st.set_page_config(
    page_title="3B Official",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

preparar_icono_pwa()
inyectar_pantalla_completa()
inyectar_css_layout_fijo()

SUPABASE_URL, SUPABASE_KEY = obtener_supabase()
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error(
        "Falta la configuración de Supabase. En local ejecuta "
        "`python generar_secrets_cloud.py`. En la nube pega los Secrets en share.streamlit.io."
    )
    st.stop()
HEADERS = headers_supabase(SUPABASE_KEY)

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "chat_destino_id" not in st.session_state:
    st.session_state.chat_destino_id = None

config = cargar_config()

if not st.session_state.autenticado:
    render_pantalla_pin(config, cargar_logo, buscar_usuario_por_pin)
    st.stop()

usuario = st.session_state.usuario
# Refrescar datos del usuario tras cambios en admin
for u in config["usuarios"]:
    if u["id"] == usuario.get("id"):
        st.session_state.usuario = u
        usuario = u
        break

st.markdown(
    '<script>document.documentElement.classList.remove("pin-page");</script>',
    unsafe_allow_html=True,
)

en_conversacion = (
    st.session_state.get("vista", "chat") == "chat"
    and st.session_state.get("chat_destino_id") is not None
)

if en_conversacion:
    _, titulo_conv, subtitulo_conv, _ = resolver_chat_destino(
        config, st.session_state.chat_destino_id
    )
    st.markdown(
        '<script>document.documentElement.classList.add("modo-chat-activo");</script>',
        unsafe_allow_html=True,
    )
    render_cabecera_fija(
        usuario, cargar_logo("36px"), titulo_chat=titulo_conv, subtitulo_chat=subtitulo_conv
    )
    if st.button("←", key="volver_header", help="Volver a chats"):
        st.session_state.chat_destino_id = None
        st.markdown(
            '<script>document.documentElement.classList.remove("modo-chat-activo");</script>',
            unsafe_allow_html=True,
        )
        st.rerun()
    espaciador_contenido()
else:
    st.markdown(
        '<script>document.documentElement.classList.remove("modo-chat-activo");</script>',
        unsafe_allow_html=True,
    )
    render_cabecera_fija(usuario, cargar_logo("40px"))
    barra_navegacion(usuario)
    espaciador_contenido()

if st.session_state.vista == "admin" and es_admin(usuario):
    pantalla_admin(config)
else:
    pantalla_chat(usuario, config)
