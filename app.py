import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, auth, firestore
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
import time

# Inicialização do Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Função de autenticação
def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except:
        return None

# Página de login
def show_login():
    st.title("NutraFlex")
    st.subheader("Acesse sua conta")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar", use_container_width=True):
        uid = login(email, password)
        if uid:
            st.session_state["user_uid"] = uid
            st.session_state["email"] = email
            st.rerun()
        else:
            st.error("Usuário não encontrado.")

# Página principal
def show_main():
    st.markdown("<h1 style='color:#2e7d32'>Personal Particular 💪</h1>", unsafe_allow_html=True)
    st.write("Converse com sua IA para montar dieta, treino e agenda personalizada.")
    chat = st.chat_input("Digite sua mensagem...")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if chat:
        st.session_state.chat_history.append({"role": "user", "content": chat})
        with st.chat_message("user"):
            st.markdown(chat)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                res = requests.post("https://nutraflex-api.onrender.com/chat", json={"prompt": chat})
                reply = res.json().get("reply", "Erro ao obter resposta.")
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Roteamento
if "user_uid" not in st.session_state:
    show_login()
else:
    show_main()