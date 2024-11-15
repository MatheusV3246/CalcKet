import streamlit as st
import sqlite3

class Sessao: 
    def __init__(self):
        # Conectando ao SQLite (ou criando o banco de dados em um arquivo)
        self.conn = sqlite3.connect('Data/bd_prec.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Criando a tabela de usuários, caso ainda não exista, com as colunas adicionais
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                email TEXT PRIMARY KEY,
                senha_hash TEXT,
                nome TEXT,
                numero_pa TEXT,
                nome_pa TEXT,
                perfil TEXT
            )
        ''')
        self.conn.commit()
            
    def fechar_con(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
        
    def obter_dados_usuarios(self):
        """Obtém os dados do usuário logado a partir do email na sessão."""
        try:
            email = st.session_state.get('email', "")
            # Recupera nome, número PA, nome PA e perfil do usuário com o email especificado
            dados = self.cursor.execute('SELECT nome, numero_pa, nome_pa, perfil FROM usuarios WHERE email = ?', (email,)).fetchone()
            if dados:
                return dados
            else:
                st.warning("Nenhum usuário encontrado.")
                return None
        except Exception as e:
            st.error(f"Erro ao recuperar usuários: {str(e)}")
            return None
