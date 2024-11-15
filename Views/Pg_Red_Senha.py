import streamlit as st
import sqlite3
from Controllers.Auth_Ver import Autorizacao

class Redefinir(Autorizacao):   
    def __init__(self):
        super().__init__()
        # Conectando ao SQLite (ou criando o banco de dados em um arquivo)
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
        
        self.mostrar_redefinir()
        
    def mostrar_redefinir(self):
        email = st.session_state.get('email', "")
        senha = st.text_input("Senha (Antiga):", type="password")
        senha2 = st.text_input("Senha (Repita a Senha Antiga):", type="password")
        senha_nova = st.text_input("Senha (Nova):", type="password")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            btn_redefinir = st.button("Redefinir Senha")
        
        if btn_redefinir:
            if senha == senha2:
                result = self.verificar_login(email, senha)
                if result and senha_nova:
                    senha_hash_nova = self.hash_senha(senha_nova)
                    self.cursor.execute('UPDATE usuarios SET senha_hash = ? WHERE email = ?', (senha_hash_nova, email))
                    self.conn.commit()
                    st.success("Senha redefinida com sucesso!")
                else:
                   st.warning("Senha incorreta ou nova senha inválida!")             
            else:
                st.warning("As senhas não correspondem!")
                
    def verificar_login(self, email, senha):
        """Verifica se o login é válido comparando o hash da senha."""
        senha_hash = self.hash_senha(senha)
        result = self.cursor.execute('SELECT senha_hash FROM usuarios WHERE email = ?', (email,)).fetchone()
        return result and result[0] == senha_hash
