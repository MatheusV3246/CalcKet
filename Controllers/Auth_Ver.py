import streamlit as st
from functools import wraps
import hashlib

class Autorizacao:
    @staticmethod
    def get_perfil():
        # Obtém o perfil do estado da sessão
        return st.session_state.get('perfil')

    # Decorador para verificar se o usuário é admin
    @staticmethod
    def isAdmin(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if Autorizacao.get_perfil() == "admin":
                return func(*args, **kwargs)
            else:
                st.warning("Você não possui permissão para acessar esta página.")
                return None
        return wrapper
    
    # Decorador para verificar se o usuário é agente
    @staticmethod
    def isAgent(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if Autorizacao.get_perfil() == "agent":
                return func(*args, **kwargs)
            else:
                st.warning("Você não possui permissão para acessar esta página.")
                return None
        return wrapper
    
    def hash_senha(self, senha):
        """Retorna o hash SHA-256 da senha fornecida."""
        return hashlib.sha256(senha.encode()).hexdigest()