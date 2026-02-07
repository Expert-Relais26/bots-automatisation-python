import streamlit as st
from openai import OpenAI

# 1. Configuration de la page
st.set_page_config(page_title="Mon Agent IA", page_icon="🤖")
st.title("🤖 Mon interface IA")

# 2. Connexion à la clé API (que tu as mise dans les Secrets)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("Clé API manquante ou invalide dans les Secrets.")
    st.stop()

# 3. Gestion des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Zone de discussion
if prompt := st.chat_input("Posez votre question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        )
        content = response.choices[0].message.content
        st.markdown(content)
    st.session_state.messages.append({"role": "assistant", "content": content})