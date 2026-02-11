import streamlit as st
from openai import OpenAI

# Configuration de la page
st.set_page_config(page_title="Mon Hub d'Experts", layout="wide")

# Récupération de la clé API (On la configurera dans Streamlit Cloud)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🚀 Mon Hub d'Experts Digital")

# Liste de tes 10 experts
experts = {
    "Le Détecteur d'Opportunités (Audit)": "Tu es un expert en audit business. Analyse cette idée et trouve les failles.",
    "L'Aimant à Clients (Stratégie)": "Tu es un expert en acquisition client. Comment attirer du monde ?",
    "La Plume de Vente (Copywriting)": "Tu es un expert en rédaction de vente. Rédige un texte persuasif.",
    "Le Réalisateur TikTok/Reels": "Tu es un expert en scripts vidéo courts et viraux.",
    "Le Conclueur (Vente/Closing)": "Tu es un expert en closing. Comment répondre à cette objection ?",
    "L'Automatisateur (IA Business)": "Tu es un expert en automatisation. Quel outil utiliser pour gagner du temps ?",
    "Le Propulseur (Publicité Ads)": "Tu es un expert en Facebook et Google Ads.",
    "Le Maître de Google (SEO)": "Tu es un expert en référencement naturel.",
    "Le Stratège Email": "Tu es un expert en marketing par email.",
    "Le Designer d'Offres": "Tu es un expert en création d'offres irrésistibles."
}

# Barre latérale pour choisir l'expert
with st.sidebar:
    st.header("Configuration")
    choix_expert = st.selectbox("Sélectionnez votre expert :", list(experts.keys()))
    st.write(f"**Expert actif :** {choix_expert}")

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Posez votre question à l'expert..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Appel réel à l'IA avec le rôle de l'expert choisi
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": experts[choix_expert]},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})