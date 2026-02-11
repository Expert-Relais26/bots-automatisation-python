import streamlit as st

st.set_page_config(page_title="Mon Hub d'Experts IA", layout="centered")

st.title("🚀 Mon Hub d'Experts Digital")
st.markdown("---")

# --- CONFIGURATION DE TES 10 EXPERTS ---
MES_BOTS = {
    "Le Détecteur d'Opportunités (Audit Malt)": "8029c633-f7c2-4303-a822-7d95227db76a-a212aed4-1bca-4e9a-b482-0b0b29d18c70",
    "L'Aimant à Clients (Stratégie LinkedIn)": "8029c633-f7c2-4303-a822-7d95227db76a-b165701d-e588-4450-adfc-ced2b5dcdde1",
    "La Plume de Vente (Copywriting)": "8029c633-f7c2-4303-a822-7d95227db76a-2476d135-d42b-4378-b7f0-02a961b805b7",
    "Le Réalisateur TikTok/Reels (Scripts)": "8029c633-f7c2-4303-a822-7d95227db76a-642f686a-eede-4c81-ab03-62d9410231b0",
    "Le Conclueur (Vente/Closing)": "8029c633-f7c2-4303-a822-7d95227db76a-7275fe71-2783-4a69-beac-f735cecc12c6",
    "L'Automatisateur (IA Business)": "8029c633-f7c2-4303-a822-7d95227db76a-09372bd4-096b-4b6d-98fb-8b9e1099867e",
    "Le Propulseur (Publicité Ads)": "8029c633-f7c2-4303-a822-7d95227db76a-50d5752b-63ab-4e26-a3bd-fc6a8c262b66",
    "Le Maître de Google (SEO)": "8029c633-f7c2-4303-a822-7d95227db76a-a472391a-fbd9-4a7f-89e3-50a6d89adeaf",
    "Le Conteur de Marque (Storytelling)": "8029c633-f7c2-4303-a822-7d95227db76a-fd7f0732-faff-4a9a-9a6b-6357b4f89b22",
    "Le Calculateur de Profit (Prix/Offre)": "8029c633-f7c2-4303-a822-7d95227db76a-7b64843e-e550-45ab-a0c1-33088b3df59e"
}

# Sélection de l'expert
choix_expert = st.sidebar.selectbox("Sélectionnez votre expert :", list(MES_BOTS.keys()))
id_expert = MES_BOTS[choix_expert]

st.sidebar.info(f"Expert actif : \n\n*{choix_expert}*")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Posez votre question à l'expert..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Note : La connexion API sera finalisée demain avec ta clé
    with st.chat_message("assistant"):
        st.markdown(f"*{choix_expert}* est prêt à vous répondre. (Connexion API en attente d'activation)")