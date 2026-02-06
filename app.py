import streamlit as st
import time

# 1. Configuration de l'apparence (Page Web)
st.set_page_config(page_title="Research Expert", page_icon="🔍")

# Design personnalisé pour ressembler à tes images
st.markdown("""
<style>
    .stApp { background-color: #1E1E1E; color: white; }
    .subtitle { text-align: center; color: #4CAF50; font-size: 0.9em; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 2. Sécurité : Mot de passe pour protéger ton travail sur Malt
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Accès Research Expert")
    mdp = st.text_input("Veuillez entrer la clé d'accès", type="password")
    if st.button("Se connecter"):
        if mdp == "MALT2026": 
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Clé incorrecte.")
else:
    # 3. Ton Interface "Research Expert"
    st.markdown("<h1 style='text-align: center;'>🔍 Research Expert</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Propulsé par Relais 26</p>', unsafe_allow_html=True)

    # Historique du chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    # Zone de saisie (Implantation de l'IA)
    if prompt := st.chat_input("Posez votre question ici..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Ici, le robot répond !
            response = f"*Research Expert :* J'analyse votre demande sur '{prompt}'... Système prêt."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
  # --- SECTION REDIRECTION MALT ---
st.sidebar.markdown("---") 
st.sidebar.write("### 🚀 Service Professionnel")
st.sidebar.info("Cette version de démonstration est limitée à quelques tests.")

# Remplace le lien entre guillemets par ton vrai lien de profil Malt plus tard
url_malt = "https://www.malt.fr" 
st.sidebar.link_button("Commander l'analyse complète sur Malt", url_malt)