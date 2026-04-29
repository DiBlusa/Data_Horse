import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from User.SDB_User import check_user_credentials


# Configuração da página
st.set_page_config(
    page_title="Data Horse - Login",
    page_icon="🐴",
    layout="centered"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        background-color: #f0f0f0;
    }
    .login-container {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .title {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None


def login():
    """Valida as credenciais e faz login."""
    username = st.session_state.username.strip()
    password = st.session_state.password
    
    # Validação básica
    if not username or not password:
        st.warning("Por favor, preencha os campos de usuário e senha.")
        return
    
    # Verifica credenciais
    user = check_user_credentials(username, password)
    
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user
        st.success(f"Bem-vindo, {user.username}!\nPapel: {user.role.name}")
    else:
        st.error("Usuário ou senha incorretos.")
        st.session_state.password = ""


# Página principal de login
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='title'>🐴 data_horse</h1>", unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            st.text_input(
                "Name",
                key="username",
                placeholder="Digite seu usuário"
            )
            
            st.text_input(
                "Password",
                type="password",
                key="password",
                placeholder="Digite sua senha"
            )
            
            submitted = st.form_submit_button(
                "Login",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                login()
else:
    # Página após login
    st.success(f"✅ Bem-vindo, {st.session_state.user.username}!")
    st.info(f"Papel: {st.session_state.user.role.name}")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
