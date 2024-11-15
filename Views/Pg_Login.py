import streamlit as st
import sqlite3
from Controllers.Auth_Ver import Autorizacao
import base64
from streamlit_cookies_manager import EncryptedCookieManager

class Login(Autorizacao):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('Data/bd_prec.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Criando a tabela de usuários, caso ainda não exista, com as colunas adicionais
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                email TEXT PRIMARY KEY,
                senha_hash TEXT,
                nome TEXT,
                perfil TEXT
            )
        ''')
        self.conn.commit()

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

        # Carrega o logo em base64 para exibição
        with open("Images/Logo.png", "rb") as logo_file:
            self.logo_b64 = base64.b64encode(logo_file.read()).decode()

    def criar_tela(self):
        """Exibe o layout da tela de login."""
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            # Exibe o logo no centro da coluna
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
            """, unsafe_allow_html=True)
            
            email = st.text_input("Email", value=st.session_state['email'])
            senha = st.text_input("Senha", type="password")
            
            # Botão de login centralizado
            c1, c2, c3 = st.columns(3)
            with c2:
                if st.button("Login", type="primary", disabled=not senha):
                    if email and senha:
                        self.logar(email, senha)
                    else:
                        st.warning("Por favor, preencha ambos os campos.")

            # Mensagem de erro de login
            if st.session_state['login_failed']:
                st.error("Falha no login: Email ou senha incorretos.")

    def logar(self, email, senha):
        """Verifica as credenciais e realiza login."""
        login = self.verificar_login(email, senha)
        if login:
            st.session_state['logged_in'] = True
            st.session_state['email'] = email
            st.session_state['login_failed'] = False

            # Armazena o estado de login e o email nos cookies
            self.cookies["logged_in"] = "true"
            self.cookies["email"] = email
            self.cookies.save()
            st.success("Login realizado com sucesso!")
        else:
            st.session_state['login_failed'] = True

    def verificar_login(self, email, senha):
        """Verifica se o login é válido comparando o hash da senha."""
        senha_hash = self.hash_senha(senha)
        result = self.conn.execute('SELECT senha_hash FROM usuarios WHERE email = ?', (email,)).fetchone()
        return result and result[0] == senha_hash

    def logout(self):
        """Realiza logout e limpa os cookies e a sessão."""
        st.session_state['logged_in'] = False
        st.session_state['email'] = ""
        self.cookies["logged_in"] = "false"
        self.cookies["email"] = ""
        self.cookies.save()
        st.success("Logout realizado com sucesso!")
