import streamlit as st
import sqlite3
from Controllers.Auth_Ver import Autorizacao
import base64
from streamlit_cookies_manager import EncryptedCookieManager

class Login(Autorizacao):
    def __init__(self):
        Autorizacao.__init__(self)
        caminho = "Data/bd_users.db"
        self.conn = sqlite3.connect(caminho, check_same_thread=False)

        # Inicializa o gerenciador de cookies
        self.cookies = EncryptedCookieManager(
            prefix="login_app",
            password="MTHV"
        )
        if not self.cookies.ready():
            st.stop()
        
        # Inicializa as variáveis de sessão para controle de login e email
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = self.cookies.get("logged_in") == "true"
            
        if 'email' not in st.session_state:
            st.session_state['email'] = self.cookies.get("email", "")
            
        if 'login_failed' not in st.session_state:
            st.session_state['login_failed'] = False

        with open("Images/Logo_Branco.png", "rb") as logo_file:
            self.logo_b64 = base64.b64encode(logo_file.read()).decode()
            
    def criar_tela(self):
        # Layout do login
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.markdown(f"""
                <div style="
                        content: '';
                        display: block;
                        height: 130px;
                        width: 100%;
                        background-image: url('data:image/png;base64,{self.logo_b64}');
                        background-size: contain;
                        background-repeat: no-repeat;
                        background-position: center;
                        margin-bottom: 30px;">
                </div>
            """,unsafe_allow_html=True)
            
            email = st.text_input("Email", value=st.session_state.get('email',''))
            senha = st.text_input("Senha", type="password")
        
            st.button("Login", type="primary", disabled=not senha, on_click=lambda: self.logar(email, senha), use_container_width=True)

    def logar(self, email, senha):
        login = self.verificar_login(email, senha)
        if login:
            st.session_state['logged_in'] = True
            st.session_state['email'] = email
            st.session_state['login_failed'] = False
            st.session_state['button_clicked'] = False

            # Armazena o estado de login e o email nos cookies
            self.cookies["logged_in"] = "true"
            self.cookies["email"] = email
            self.cookies.save()
        else:
            st.session_state['login_failed'] = True
            st.warning("Senha incorreta!")

    def verificar_login(self, email, senha):
        """Verifica se o login é válido comparando o hash da senha."""
        senha_hash = self.hash_senha(senha)
        cursor = self.conn.cursor()
        result = cursor.execute('SELECT senha_hash FROM usuarios WHERE email = ?', (email,)).fetchone()
        
        return result and result[0] == senha_hash

    def logout(self):
        """Realiza logout e limpa os cookies e a sessão."""
        st.session_state['logged_in'] = False
        st.session_state['email'] = ""
        self.cookies["logged_in"] = "false"
        self.cookies["email"] = ""
        self.cookies.save()
