import streamlit as st
import sqlite3  # Substituindo DuckDB por SQLite para acessos simultâneos
import pandas as pd
from Controllers.Auth_Ver import Autorizacao

class Usuarios(Autorizacao):   
    def __init__(self):
        Autorizacao.__init__(self)
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
    
    def mostrar_painel_controle(self):
        self.registrar_novo_usuario()
        self.editar_usuario()
        self.apagar_usuario()
        
    def registrar_novo_usuario(self):
        with st.expander("Registrar Usuário"):
            """Tela para registrar novos usuários."""
                
            # Campos de E-mail, Senha, Nome, Número PA e Nome PA para registro
            email = st.text_input("Email:")
            senha = st.text_input("Senha:", type="password")
            nome = st.text_input("Nome:")
            numero_pa = st.selectbox("Número PA", ["1", "2", "3", "4", "5", "6", 
                                    "7", "8", "9", "10", "11","97", "99"], index=None)
                
            nome_pa = st.selectbox("Nome PA:", ["Anápolis", "Castelo Branco", "OCB", "CASAG", "POA", "Caxias do Sul", 
                                    "Goianira", "Cuiabá", "Campo Grande", "Taguatinga", "Sede","Digital", "UAD"], index=None)
                
            perfil = st.selectbox("Perfil:", ["user", "agent", "admin"])
                
            # Botão para registrar
            if st.button("Registrar"):
                if email and senha and nome and numero_pa and nome_pa and perfil:
                    self.registrar_usuario(email, senha, nome, numero_pa, nome_pa, perfil)
                else:
                    st.error("Por favor, preencha todos os campos.")  
                           
    def registrar_usuario(self, email, senha, nome, numero_pa, nome_pa, perfil):
        """Registra um novo usuário com o email, senha criptografada e informações adicionais."""
        senha_hash = self.hash_senha(senha)
        try:
            self.cursor.execute('INSERT INTO usuarios (email, senha_hash, nome, numero_pa, nome_pa, perfil) VALUES (?, ?, ?, ?, ?, ?)', 
                            (email, senha_hash, nome, numero_pa, nome_pa, perfil))
            self.conn.commit()
            st.success(f"Usuário {email} registrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao registrar usuário: {str(e)}")
        # Atualiza a lista de usuários após o registro
        self.mostrar_usuarios()
        
    def apagar_usuario(self):
        with st.expander("Apagar Usuário"):
            email = st.text_input("Email do Usuário para apagar")
            if st.button("Apagar Usuário"):
                if email:
                    try:
                        self.cursor.execute('DELETE FROM usuarios WHERE email = ?', (email,))
                        self.conn.commit()
                        st.success(f"Usuário {email} apagado com sucesso!")
                        self.mostrar_usuarios()
                    except Exception as e:
                        st.error(f"Erro ao apagar usuário: {str(e)}")
                else:
                    st.error("Por favor, preencha o campo de email.")

    def editar_usuario(self):
        with st.expander("Editar Usuário"):
            email_antigo = st.text_input("Email do Usuário")
            st.info("Preencha os campos que deseja editar, caso deseje manter, deixe em branco!")

            email_novo = st.text_input("Email (Novo):")
            senha_nova = st.text_input("Senha (Novo):", type="password")
            nome = st.text_input("Nome (Novo):")
            numero_pa = st.selectbox("Número PA (Novo):", ["1", "2", "3", "4", "5", "6", 
                                    "7", "8", "9", "10", "11","97"], index=None)
                
            nome_pa = st.selectbox("Nome PA (Novo):", ["Anápolis", "Castelo Branco", "OCB", "CASAG", "POA", "Caxias do Sul", 
                                    "Goianira", "Cuiabá", "Campo Grande", "Taguatinga", "Sede","Digital"], index=None)
                
            perfil = st.selectbox("Perfil (Novo):", ["user", "admin"])

            if st.button("Editar Usuário"):
                if email_antigo:
                    try:
                        if email_novo:
                            self.cursor.execute('UPDATE usuarios SET email = ? WHERE email = ?', (email_novo, email_antigo))
                        if senha_nova:
                            senha_hash_nova = self.hash_senha(senha_nova)
                            self.cursor.execute('UPDATE usuarios SET senha_hash = ? WHERE email = ?', (senha_hash_nova, email_novo or email_antigo))
                        if nome:
                            self.cursor.execute('UPDATE usuarios SET nome = ? WHERE email = ?', (nome, email_novo or email_antigo))
                        if numero_pa:
                            self.cursor.execute('UPDATE usuarios SET numero_pa = ? WHERE email = ?', (numero_pa, email_novo or email_antigo))
                        if nome_pa:
                            self.cursor.execute('UPDATE usuarios SET nome_pa = ? WHERE email = ?', (nome_pa, email_novo or email_antigo))
                        if perfil:
                            self.cursor.execute('UPDATE usuarios SET perfil = ? WHERE email = ?', (perfil, email_novo or email_antigo))
                        self.conn.commit()
                        st.success(f"Usuário {email_antigo} atualizado com sucesso!")
                        self.mostrar_usuarios()
                    except Exception as e:
                        st.error(f"Erro ao atualizar usuário: {str(e)}")
                    else:
                        st.error("Por favor, preencha o campo de email.")
                
    def mostrar_usuarios(self):
        with st.container():
            st.markdown("<h2 style='text-align: center; color: #C9D200;'>Usuários Registrados</h2>", unsafe_allow_html=True)
                
            try:
                usuarios = self.cursor.execute('SELECT email, perfil FROM usuarios').fetchall()
                    
                if usuarios:
                    df = pd.DataFrame(usuarios, columns=['Email', 'Perfil'])
                    st.dataframe(df.style.hide(axis='index'), use_container_width=True)
                else:
                    st.warning("Nenhum usuário encontrado.")
            except Exception as e:
                st.error(f"Erro ao recuperar usuários: {str(e)}")
                           
    def mostrar_todas_simulacao(self):
        with st.container():
            st.markdown("<h2 style='text-align: center; color: #C9D200;'>Simulações Registradas</h2>", unsafe_allow_html=True)    
            try:
                simulacoes = self.ler_simulacao()
                
                if simulacoes:
                    df = pd.DataFrame(simulacoes, columns=['Nº SIM', 'Taxa', 'Tabela', 'Natureza', 
                                                           'Risco', 'Linha', 'Nº Linha', 'Prazo Máx', 'Nome Cliente', 
                                                           'Nome Gerente', 'Nome PA', 'Nº PA', 'Email', 'Defesa', 
                                                           'Amortização', 'Crédito', 'Prazo', 'Parcela', 'CET'])
                    st.dataframe(df.style.hide(axis='index'), use_container_width=True)
                else:
                    st.warning("Nenhuma simulação cadastrada.")
            except Exception as e:
                st.error(f"Erro ao recuperar simulações: {str(e)}")


