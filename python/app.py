import streamlit as st
import requests
import json

st.set_page_config(page_title="Chat Webex + Streamlit", page_icon="💬")

# ---------------------------
# CONFIGURACIÓN (USA TUS DATOS)
# ---------------------------
ROOM_ID = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNzk2NTE4ZTAtYzQwMy0xMWYwLTk3ZTEtOGIwYTU2Y2Y4MTll"
TOKEN = "MDA2ZDEwODMtMmE5MC00ZDhmLTgyMWQtZTIxNTNjZjA2YTU3MDUzOWM4YjUtN2Ni_P0A1_2c8af025-7907-4b20-8951-8d739b0ec3c0"  # Bot Token o user token

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

WEBEX_LIST_URL = f"https://webexapis.com/v1/messages?roomId={ROOM_ID}"
WEBEX_SEND_URL = "https://webexapis.com/v1/messages"


# --------------------------------
# Función: obtener mensajes Webex
# --------------------------------
def obtener_mensajes():
    try:
        resp = requests.get(WEBEX_LIST_URL, headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("items", [])
        else:
            st.error(f"Error al obtener mensajes: {resp.text}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []


# --------------------------------
# Función: enviar mensaje a Webex
# --------------------------------
def enviar_mensaje(texto):
    payload = {
        "roomId": ROOM_ID,
        "text": texto
    }

    try:
        resp = requests.post(WEBEX_SEND_URL, headers=HEADERS, data=json.dumps(payload))
        if resp.status_code != 200:
            st.error(f"Error enviando mensaje: {resp.text}")
    except Exception as e:
        st.error(f"Error: {e}")


# --------------------------------
# UI del chat en Streamlit
# --------------------------------
st.title("💬 Chat Integrado con Webex API")

st.markdown("Este chat web se conecta a un espacio Webex, lee mensajes y envía respuestas.")

# Mostrar historial Webex
st.subheader("📨 Mensajes desde Webex")

mensajes = obtener_mensajes()

for m in mensajes[:20]:  # mostrar últimos 20
    author = m.get("personEmail", "desconocido")
    text = m.get("text", "")

    with st.chat_message("assistant" if "bot" in author else "user"):
        st.markdown(f"**{author}:** {text}")

# Input del usuario para enviar mensaje
st.subheader("✉️ Enviar mensaje al espacio Webex")

user_input = st.chat_input("Escribe un mensaje para enviar a Webex…")

if user_input:
    enviar_mensaje(user_input)
    st.success("Mensaje enviado a Webex ✔️")
