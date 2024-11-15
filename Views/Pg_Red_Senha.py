import streamlit as st
import sqlite3
from Controllers.Auth_Ver import Autorizacao

class Redefinir(Autorizacao):   
    def __init__(self):
        Autorizacao.__init__(self)
        # Conectando ao SQLite (ou criando o banco de dados em um arquivo)
        caminho = "Data/bd_users.db"
        self.conn = sqlite3.connect(caminho, check_same_thread=False)

        # Criando a tabela de usuários, caso ainda não exista, com as colunas adicionais
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                email VARCHAR PRIMARY KEY,
                senha_hash VARCHAR,
                nome VARCHAR,
                numero_pa VARCHAR,
                nome_pa VARCHAR,
                perfil VARCHAR
            )
        ''')
        
        self.mostrar_redefinir()
        
    def mostrar_redefinir(self):
        email = st.session_state['email']
        senha = st.text_input("Senha (Antiga):", type="password")
        senha2 = senha = st.text_input("Senha (Repita a Senha Antiga):", type="password")
        senha_nova = st.text_input("Senha (Novo):", type="password")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            btn_redefinir = st.button("Redefinir Senha")
        
        if btn_redefinir:
            if senha == senha2:
                result = self.verificar_login(email, senha)
                if result and senha_nova:
                    senha_hash_nova = self.hash_senha(senha_nova)
                    self.conn.execute('UPDATE usuarios SET senha_hash = ? WHERE email = ?', (senha_hash_nova, email))
                    self.conn.commit()
                    
                    st.success("Senha redefinida com sucesso!")
                else:
                   st.warning("Senha incorreta!")             
            else:
                st.warning("As senhas não correspondem!")
                
    def verificar_login(self, email, senha):
        """Verifica se o login é válido comparando o hash da senha."""
        senha_hash = self.hash_senha(senha)
        cursor = self.conn.cursor()

        result = cursor.execute('SELECT senha_hash FROM usuarios WHERE email = ?', (email,)).fetchone()
        return result and result[0] == senha_hash