"""Configuración local y en Streamlit Cloud (secrets + sesión)."""

import json
import os
import uuid
from pathlib import Path

import streamlit as st

_CONFIG_SS = "_config_3b_datos"
_AVISO_NUBE_SS = "_aviso_nube_config_mostrado"

# Valores por defecto solo para desarrollo local sin secrets.toml
_DEFAULT_SUPABASE_URL = "https://yckvxerrxgeqxzqtepdk.supabase.co"
_DEFAULT_SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlja3Z4ZXJyeGdlcXh6cXRlcGRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg4OTU4OTcsImV4cCI6MjA5NDQ3MTg5N30."
    "vNcyZ7NIGkh3GH7JUyz1S8RQh5JBO-c_AKiU_rj5LJQ"
)


def ruta_config():
    return Path(__file__).resolve().parent / "usuarios_pin.json"


def es_streamlit_cloud():
    return os.environ.get("STREAMLIT_RUNTIME_ENVIRONMENT") == "cloud"


def config_persistente_en_disco():
    if es_streamlit_cloud():
        return False
    ruta = ruta_config()
    try:
        if ruta.is_file():
            with open(ruta, "r+", encoding="utf-8") as f:
                f.seek(0, 2)
        else:
            ruta.write_text("{}", encoding="utf-8")
        return True
    except OSError:
        return False


def obtener_supabase():
    url, key = "", ""
    try:
        if "supabase" in st.secrets:
            url = str(st.secrets["supabase"].get("url", "") or "").strip()
            key = str(st.secrets["supabase"].get("key", "") or "").strip()
    except Exception:
        pass

    if not url or not key:
        url = os.environ.get("SUPABASE_URL", _DEFAULT_SUPABASE_URL).strip()
        key = os.environ.get("SUPABASE_KEY", _DEFAULT_SUPABASE_KEY).strip()

    return url, key


def headers_supabase(api_key):
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def normalizar_usuario(u):
    u = dict(u)
    u.setdefault("id", uuid.uuid4().hex[:8])
    u.setdefault("activo", True)
    u.setdefault("admin", False)
    u.setdefault("puesto", "Tienda")
    return u


def _config_desde_secrets():
    try:
        if "usuarios_pin_json" in st.secrets:
            raw = st.secrets["usuarios_pin_json"]
            if isinstance(raw, str):
                return json.loads(raw)
            return dict(raw)
        if "usuarios_pin" in st.secrets:
            data = dict(st.secrets["usuarios_pin"])
            usuarios = data.get("usuarios", [])
            if usuarios is not None and not isinstance(usuarios, list):
                usuarios = list(usuarios)
            data["usuarios"] = [normalizar_usuario(dict(u)) for u in (usuarios or [])]
            return data
    except Exception:
        pass
    return None


def cargar_config():
    if _CONFIG_SS in st.session_state:
        return st.session_state[_CONFIG_SS]

    data = _config_desde_secrets()

    if not data or not data.get("usuarios"):
        ruta = ruta_config()
        if ruta.is_file():
            data = json.loads(ruta.read_text(encoding="utf-8"))

    if not data or not data.get("usuarios"):
        data = {
            "pin_longitud": 4,
            "usuarios": [
                {
                    "id": "admin01",
                    "nombre": "Andrés",
                    "pin": "1001",
                    "puesto": "Encargado",
                    "admin": True,
                    "activo": True,
                },
            ],
        }

    data["pin_longitud"] = int(data.get("pin_longitud", 4))
    data["usuarios"] = [normalizar_usuario(dict(u)) for u in data["usuarios"]]
    st.session_state[_CONFIG_SS] = data
    return data


def guardar_config(config):
    st.session_state[_CONFIG_SS] = config
    if config_persistente_en_disco():
        ruta = ruta_config()
        ruta.write_text(
            json.dumps(config, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return True
    return False


def aviso_admin_en_nube():
    if not es_streamlit_cloud():
        return
    if st.session_state.get(_AVISO_NUBE_SS):
        return
    st.session_state[_AVISO_NUBE_SS] = True
    st.info(
        "**App en la nube:** los cambios de empleados/PIN duran mientras uses la app. "
        "Para guardarlos de forma permanente, actualiza **Secrets** en "
        "[share.streamlit.io](https://share.streamlit.io) con el contenido de "
        "`secrets_para_nube.toml` (generado con `python generar_secrets_cloud.py`)."
    )
