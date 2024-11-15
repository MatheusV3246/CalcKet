import streamlit as st
import pandas as pd
import glob
import base64
st.set_page_config(
    layout="wide", 
    page_title="CalcKet",
    page_icon="🏦"
)
from Controllers.Auth_Ver import Autorizacao
from Controllers.Ger_Sessao import Sessao
from Views.Pg_Login import Login
from Views.Pg_Calc import Calc
from Views.Pg_Controle import Usuarios
from Views.Pg_Red_Senha import Redefinir
from time import sleep

# Configuração da imagem de fundo e logotipo
with open("Images/fundo.png", "rb") as img_file:
    image_b64 = base64.b64encode(img_file.read()).decode()
with open("Images/logo_SAM.png", "rb") as logo_sam_file:
    logo_sam_b64 = base64.b64encode(logo_sam_file.read()).decode()
with open("Images/Logo.png", "rb") as logo_file:
    logo_b64 = base64.b64encode(logo_file.read()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{image_b64}");
        background-size: cover;
    }}

    [data-testid="stSidebar"] {{
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }}

    [data-testid="stSidebar"]::before {{
        content: "";
        display: block;
        height: 180px;
        width: 200%;
        background-image: url("data:image/png;base64,{logo_sam_b64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        margin-top: 20px;
    }}
        
    [data-testid="stSidebar"]::after {{
        content: "";
        display: block;
        height: 100px;
        width: 100%;
        background-image: url("data:image/png;base64,{logo_b64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        margin-bottom: 30px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 30Px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

class SAM_UI(Login, Autorizacao, Sessao):
    def __init__(self):
        Login.__init__(self)
        Sessao.__init__(self)
        Autorizacao.__init__(self)
        self.users = Usuarios()
        self.inicializar_sessao()

    def inicializar_sessao(self):
        if 'logged_in' in st.session_state and st.session_state['logged_in']:
            self.obter_dados()
            self.inicializar_app()
            self.fechar_con()
        else:
            self.criar_tela()
            
    def obter_dados(self):
        dados = self.obter_dados_usuarios()
        st.session_state['nome'] = dados[0]
        st.session_state['numero_pa'] = dados[1]
        st.session_state['nome_pa'] = dados[2]
        st.session_state['perfil'] = dados[3]
    
    def inicializar_app(self):
        with st.sidebar:
            st.write(f"Nome: {st.session_state['nome']}")
            st.write(f"Email: {st.session_state['email']}")
            st.write(f"Agência: {st.session_state['nome_pa']} | Nº: {st.session_state['numero_pa']}")
            st.write(f"Perfil: {st.session_state['perfil']}")
                  
            pages = {
                "Visões": [
                    st.Page("Views/Pg_Calc.py", title="Home", icon="🏠"),
                    st.Page("Views/Pg_Red_Senha.py", title="Redefinir", icon="📝"),
                    st.Page("Views/Pg_Controle.py", title="Controles", icon="⚙️"),
                ],
            }
                    
            pg = st.navigation(pages, position="sidebar")
            
            cs1, cs2, cs3 = st.columns(3)
            with cs2:
                if st.button("Encerrar"):
                    self.logout()
                    st.rerun()

            st.write("Desenvolvido por Matheus Vicente")
                    
        # Renderiza a página ativa com base no título selecionado
        if pg.title == "Home":
            with st.spinner("Carregando.."):
                Calc()
                sleep(2)
                
        elif pg.title == "Redefinir":
            with st.spinner("Carregando.."):
                Redefinir()
                sleep(2)
           
        elif pg.title == "Controles":
            with st.spinner("Carregando.."):
                self.mostrar_painel()
                sleep(2)
              
    @Autorizacao.isAdmin
    def mostrar_painel(self):
        self.users.mostrar_painel_controle()
        
if __name__ == "__main__":
    SAM_UI()
