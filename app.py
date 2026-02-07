import streamlit as st
from openai import OpenAI

# Configuration de l'interface
st.set_page_config(page_title="Mon Agent IA", page_icon="🤖")
st.title("🤖 Mon interface IA")

# Connexion à la clé API (via les Secrets Streamlit)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Erreur de configuration de la clé API.")
    st.stop()

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur
if prompt := st.chat_input("Posez votre question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Utilisation du modèle gpt-4o-mini pour éviter l'erreur 404
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        )
        content = response.choices[0].message.content
        st.markdown(content)
    st.session_state.messages.append({"role": "assistant", "content": content})