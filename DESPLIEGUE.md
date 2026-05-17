# 3B OFFICIAL — usar desde cualquier red (Streamlit Cloud)

Con esto la app queda en una URL pública (HTTPS). Funciona con WiFi, datos móviles u otra sucursal. **No hace falta tener la PC encendida.**

---

## Hoy (5 minutos en tu PC)

### 1. Generar los Secrets

En la carpeta del proyecto:

```bat
python generar_secrets_cloud.py
```

Se crean:

- `.streamlit/secrets.toml` — para seguir probando en tu PC
- `secrets_para_nube.toml` — **lo pegarás mañana en Streamlit Cloud**

### 2. Subir el proyecto a GitHub

1. Crea un repositorio en [github.com](https://github.com) (**recomendado: privado**).
2. Sube toda la carpeta `MENSAJERO` (sin `.streamlit/secrets.toml` ni `secrets_para_nube.toml`; ya están en `.gitignore`).

Si no tienes Git instalado, en GitHub: **Add file → Upload files** y arrastra los archivos del proyecto.

---

## Mañana (prueba desde el celular)

### 3. Publicar en Streamlit Cloud

1. Entra a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub.
2. **Create app** → elige tu repositorio.
3. **Main file path:** `app_chat_3b.py`
4. **Deploy**

### 4. Pegar Secrets (obligatorio)

1. En la app desplegada: **⚙️ Settings → Secrets**.
2. Abre en tu PC el archivo `secrets_para_nube.toml`.
3. Copia **todo** el contenido y pégalo en Secrets.
4. **Save** → **Reboot app** (o espera a que reinicie).

### 5. Probar

Abre la URL que te da Streamlit (ej. `https://mensajero-3b.streamlit.app`) en el celular **con datos móviles** (sin WiFi de la tienda).

- Entra con tu PIN como siempre.
- Chat, fotos y mensajes privados usan Supabase (ya en la nube).

---

## Importante

| Tema | Detalle |
|------|---------|
| **PC local** | `iniciar_para_celular.bat` sigue sirviendo solo en la misma WiFi. |
| **Admin en la nube** | Cambios de empleados/PIN duran la sesión. Para dejarlos fijos, vuelve a ejecutar `generar_secrets_cloud.py` y actualiza Secrets en Streamlit. |
| **PINs** | No subas `secrets_para_nube.toml` a GitHub público. |
| **PWA / pantalla completa** | En la URL de Streamlit también funciona “Añadir a pantalla de inicio”. |

---

## Si algo falla mañana

- **Pantalla en blanco o error de Supabase:** revisa que pegaste bien `secrets_para_nube.toml` en Secrets.
- **PIN no entra:** los usuarios deben estar en `usuarios_pin_json` dentro de Secrets (el script los copia desde `usuarios_pin.json`).
- **Chat privado o fotos:** en Supabase ejecuta los SQL `supabase_chat_privado.sql` y `supabase_fotos_temp.sql` (una sola vez).

---

## Resumen rápido

```
PC hoy:     python generar_secrets_cloud.py  →  subir a GitHub
Mañana:     share.streamlit.io  →  app_chat_3b.py  →  Secrets  →  probar URL en el celular
```
