"""Lógica de chat general y mensajes privados 1 a 1."""

import datetime
import html as html_lib
import re
import uuid
import requests
import streamlit as st

CHAT_GENERAL_ID = "__general__"
_CACHE_PRIVADO_OK = "_supabase_privado_ok"
_CACHE_FOTOS_OK = "_supabase_fotos_ok"

BUCKET_FOTOS = "chat-fotos"
FOTO_MAX_BYTES = 5 * 1024 * 1024
FOTO_EXPIRA_HORAS = 24
FOTO_TIPOS = {"image/jpeg", "image/png", "image/webp"}
FOTO_EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}


def supabase_soporta_privado(supabase_url, headers):
    if _CACHE_PRIVADO_OK in st.session_state:
        return st.session_state[_CACHE_PRIVADO_OK]
    try:
        r = requests.get(
            f"{supabase_url}/rest/v1/mensajes_chat?select=destinatario&limit=0",
            headers=headers,
            timeout=8,
        )
        ok = r.status_code == 200
    except Exception:
        ok = False
    st.session_state[_CACHE_PRIVADO_OK] = ok
    return ok


def aviso_configurar_supabase_privado():
    st.error(
        "**El chat privado no está activo en Supabase.** "
        "Sin la columna `destinatario`, los mensajes privados no se guardan "
        "y las conversaciones 🔒 aparecen vacías."
    )
    st.markdown(
        "1. Entra a [Supabase](https://supabase.com) → tu proyecto → **SQL Editor**.\n"
        "2. Ejecuta esta consulta (también está en `supabase_chat_privado.sql`):"
    )
    st.code(
        "ALTER TABLE mensajes_chat\nADD COLUMN IF NOT EXISTS destinatario TEXT;",
        language="sql",
    )
    st.caption("Después recarga la página o vuelve a entrar al chat.")
    if st.button("Ya ejecuté el SQL — comprobar de nuevo", key="recheck_supabase_privado"):
        st.session_state.pop(_CACHE_PRIVADO_OK, None)
        st.rerun()


def supabase_soporta_fotos(supabase_url, headers):
    if _CACHE_FOTOS_OK in st.session_state:
        return st.session_state[_CACHE_FOTOS_OK]
    ok = False
    try:
        r = requests.get(
            f"{supabase_url}/rest/v1/mensajes_chat?select=imagen_url,expira_at&limit=0",
            headers=headers,
            timeout=8,
        )
        ok = r.status_code == 200
    except Exception:
        ok = False
    st.session_state[_CACHE_FOTOS_OK] = ok
    return ok


def aviso_configurar_fotos():
    st.warning("**Fotos:** si ya ejecutaste el SQL, recarga la página (F5) o pulsa el botón de abajo.")
    st.markdown(
        "Si **aún no** lo hiciste:\n"
        "1. Abre [Supabase → SQL Editor](https://supabase.com/dashboard/project/yckvxerrxgeqxzqtepdk/sql/new)\n"
        "2. Pega el SQL de abajo y pulsa **Run**"
    )
    st.code(
        """ALTER TABLE mensajes_chat
ADD COLUMN IF NOT EXISTS imagen_url TEXT;

ALTER TABLE mensajes_chat
ADD COLUMN IF NOT EXISTS expira_at TIMESTAMPTZ;

INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES ('chat-fotos', 'chat-fotos', true, 5242880)
ON CONFLICT (id) DO UPDATE SET public = true, file_size_limit = 5242880;

DROP POLICY IF EXISTS "chat_fotos_subir" ON storage.objects;
DROP POLICY IF EXISTS "chat_fotos_ver" ON storage.objects;

CREATE POLICY "chat_fotos_subir"
ON storage.objects FOR INSERT TO anon
WITH CHECK (bucket_id = 'chat-fotos');

CREATE POLICY "chat_fotos_ver"
ON storage.objects FOR SELECT TO anon
USING (bucket_id = 'chat-fotos');""",
        language="sql",
    )
    if st.button("Ya ejecuté el SQL de fotos — comprobar de nuevo", key="recheck_supabase_fotos"):
        st.session_state.pop(_CACHE_FOTOS_OK, None)
        st.rerun()


def es_chat_general(msg):
    dest = msg.get("destinatario")
    return dest is None or str(dest).strip() == ""


def mensaje_expirado(msg):
    expira = msg.get("expira_at")
    if not expira:
        return False
    try:
        dt = datetime.datetime.fromisoformat(str(expira).replace("Z", "+00:00"))
        return dt <= datetime.datetime.now(datetime.timezone.utc)
    except Exception:
        return False


def _slug_chat(remitente, destinatario_privado):
    if destinatario_privado:
        partes = sorted(
            [re.sub(r"[^a-z0-9]+", "-", remitente.lower()),
             re.sub(r"[^a-z0-9]+", "-", destinatario_privado.lower())]
        )
        return f"priv-{'-'.join(partes)}"
    return "general"


def url_publica_foto(supabase_url, ruta_objeto):
    return f"{supabase_url}/storage/v1/object/public/{BUCKET_FOTOS}/{ruta_objeto}"


def subir_foto_storage(supabase_url, headers, datos, content_type, remitente, destinatario_privado):
    if content_type not in FOTO_TIPOS:
        return None, "Solo JPG, PNG o WEBP."
    if len(datos) > FOTO_MAX_BYTES:
        return None, "La foto debe pesar menos de 5 MB."

    ext = FOTO_EXT[content_type]
    carpeta = _slug_chat(remitente, destinatario_privado)
    nombre = f"{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    ruta = f"{carpeta}/{nombre}"

    upload_headers = {
        "apikey": headers["apikey"],
        "Authorization": headers["Authorization"],
        "Content-Type": content_type,
    }
    try:
        r = requests.post(
            f"{supabase_url}/storage/v1/object/{BUCKET_FOTOS}/{ruta}",
            headers=upload_headers,
            data=datos,
            timeout=30,
        )
        if r.status_code in (200, 201):
            return url_publica_foto(supabase_url, ruta), None
        if r.status_code == 400 and "Bucket not found" in r.text:
            return None, "Falta el bucket «chat-fotos» en Supabase. Ejecuta supabase_fotos_temp.sql."
        return None, f"No se pudo subir la foto ({r.status_code})."
    except Exception:
        return None, "Error de red al subir la foto."


def _contenido_html_mensaje(msg):
    hora = datetime.datetime.fromisoformat(
        msg["creado_at"].replace("Z", "+00:00")
    ).strftime("%H:%M")
    remitente = html_lib.escape(str(msg["remitente"]))
    imagen = (msg.get("imagen_url") or "").strip()
    texto = str(msg.get("mensaje") or "").strip()
    partes = []
    if imagen:
        url = html_lib.escape(imagen)
        partes.append(
            f'<img src="{url}" alt="Foto" style="max-width:100%;max-height:220px;'
            f'border-radius:10px;display:block;margin-bottom:4px;">'
        )
        if msg.get("expira_at"):
            partes.append('<span style="font-size:10px;opacity:0.8">📷 Foto temporal (24 h)</span><br>')
    if texto:
        partes.append(html_lib.escape(texto))
    cuerpo = "<br>".join(partes) if partes else "<em>Foto</em>"
    return cuerpo, hora, remitente


def filtrar_mensajes_chat(mensajes, usuario_actual, destinatario_privado=None, normalizar_nombre=None):
    yo = normalizar_nombre(usuario_actual)
    if destinatario_privado is None:
        return [m for m in mensajes if es_chat_general(m)]

    otro = normalizar_nombre(destinatario_privado)
    filtrados = []
    for m in mensajes:
        if es_chat_general(m):
            continue
        rem = normalizar_nombre(m["remitente"])
        dest = normalizar_nombre(m.get("destinatario", ""))
        if rem == yo and dest == otro:
            filtrados.append(m)
        elif rem == otro and dest == yo:
            filtrados.append(m)
    return filtrados


def obtener_mensajes_db(supabase_url, headers):
    try:
        url = f"{supabase_url}/rest/v1/mensajes_chat?order=creado_at.asc"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return [], f"Error al leer mensajes ({response.status_code})."
    except Exception:
        return [], "No se pudo conectar con Supabase."


def construir_mensajes_html(
    supabase_url,
    headers,
    usuario_actual,
    destinatario_privado=None,
    etiqueta_privado=False,
    normalizar_nombre=None,
):
    mensajes, error = obtener_mensajes_db(supabase_url, headers)
    if error:
        return f'<div class="msg received">{html_lib.escape(error)}</div>'

    filtrados = [
        m
        for m in filtrar_mensajes_chat(
            mensajes, usuario_actual, destinatario_privado, normalizar_nombre
        )
        if not mensaje_expirado(m)
    ]
    bloques = ""
    for msg in filtrados:
        cuerpo, hora, remitente = _contenido_html_mensaje(msg)
        es_propio = normalizar_nombre(msg["remitente"]) == normalizar_nombre(usuario_actual)
        if es_propio:
            bloques += f"""
            <div class="msg sent">{cuerpo}
                <div class="time">{hora} <span style="color:#7ec8ff">✓✓</span></div>
            </div>"""
        else:
            prefijo = ""
            if not etiqueta_privado:
                prefijo = f'<div class="sender">{remitente}</div>'
            bloques += f"""
            <div class="msg received">{prefijo}{cuerpo}
                <div class="time">{hora}</div>
            </div>"""

    if not bloques.strip():
        if destinatario_privado and not supabase_soporta_privado(supabase_url, headers):
            vacio = (
                "Chat privado no disponible: falta la columna destinatario en Supabase. "
                "Ejecuta supabase_chat_privado.sql en el SQL Editor del proyecto."
            )
        elif destinatario_privado:
            vacio = "Chat privado vacío. Solo ustedes dos ven lo que escriban aquí."
        else:
            vacio = "Aún no hay mensajes en el chat general."
        return f'<div class="msg received"><em>{html_lib.escape(vacio)}</em></div>'
    return bloques


def enviar_mensaje_db(supabase_url, headers, remitente, mensaje, destinatario_privado=None):
    payload = {"remitente": remitente, "mensaje": mensaje}
    if destinatario_privado:
        payload["destinatario"] = destinatario_privado
    response = requests.post(
        f"{supabase_url}/rest/v1/mensajes_chat",
        headers=headers,
        json=payload,
        timeout=10,
    )
    if response.status_code in (200, 201):
        return True, None
    if response.status_code == 400 and destinatario_privado:
        return False, (
            "Falta la columna «destinatario» en Supabase. "
            "Ejecuta supabase_chat_privado.sql en el SQL Editor."
        )
    return False, "No se pudo enviar el mensaje."


def enviar_foto_db(
    supabase_url,
    headers,
    remitente,
    imagen_url,
    destinatario_privado=None,
    mensaje_caption="",
):
    expira = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        hours=FOTO_EXPIRA_HORAS
    )
    payload = {
        "remitente": remitente,
        "mensaje": (mensaje_caption or "").strip() or "📷 Foto",
        "imagen_url": imagen_url,
        "expira_at": expira.isoformat(),
    }
    if destinatario_privado:
        payload["destinatario"] = destinatario_privado
    response = requests.post(
        f"{supabase_url}/rest/v1/mensajes_chat",
        headers=headers,
        json=payload,
        timeout=10,
    )
    if response.status_code in (200, 201):
        return True, None
    if response.status_code == 400:
        return False, (
            "Falta soporte de fotos en Supabase. Ejecuta supabase_fotos_temp.sql en el SQL Editor."
        )
    return False, "No se pudo guardar la foto en el chat."


def enviar_foto_temporal(
    supabase_url, headers, archivo, remitente, destinatario_privado=None, mensaje_caption=""
):
    if archivo is None:
        return False, "No se eligió ninguna foto."
    url, err = subir_foto_storage(
        supabase_url,
        headers,
        archivo.getvalue(),
        archivo.type or "image/jpeg",
        remitente,
        destinatario_privado,
    )
    if err:
        return False, err
    return enviar_foto_db(
        supabase_url,
        headers,
        remitente,
        url,
        destinatario_privado,
        mensaje_caption=mensaje_caption,
    )


def resolver_chat_destino(config, chat_destino_id):
    if chat_destino_id == CHAT_GENERAL_ID:
        return None, "Chat general", "Todos en la tienda", False
    for u in config["usuarios"]:
        if u["id"] == chat_destino_id:
            return u["nombre"], u["nombre"], u.get("puesto", "Tienda"), True
    return None, "Chat", "", False


def pantalla_lista_chats(
    usuario, config, usuarios_activos_fn, normalizar_nombre, supabase_url=None, headers=None
):
    st.markdown(
        """
        <script>document.documentElement.classList.add('modo-lista-chats');</script>
        <span class="lista-chats-marker" style="display:none" aria-hidden="true"></span>
        """,
        unsafe_allow_html=True,
    )

    if supabase_url and headers and not supabase_soporta_privado(supabase_url, headers):
        aviso_configurar_supabase_privado()

    if st.button(
        "Chat general de la tienda\n📢 Todos los empleados",
        use_container_width=True,
        type="secondary",
        key="abrir_general",
    ):
        st.session_state.chat_destino_id = CHAT_GENERAL_ID
        st.rerun()

    otros = sorted(
        [u for u in usuarios_activos_fn(config["usuarios"]) if u["id"] != usuario["id"]],
        key=lambda x: normalizar_nombre(x["nombre"]),
    )

    if not otros:
        st.markdown(
            '<p class="wa-aviso-vacio">No hay más empleados activos para chat privado.</p>',
            unsafe_allow_html=True,
        )
        return

    for u in otros:
        puesto = u.get("puesto", "")
        etiqueta = f"{u['nombre']}"
        if puesto:
            etiqueta += f"\n{puesto}"
        else:
            etiqueta += "\nMensaje privado"
        if st.button(etiqueta, key=f"abrir_chat_{u['id']}", use_container_width=True):
            st.session_state.chat_destino_id = u["id"]
            st.rerun()

