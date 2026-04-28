import streamlit as st

# Configuração inicial
st.set_page_config(
    page_title="RegeIT - Gestão de Equipamentos",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)
#Logo
try:
    st.sidebar.image("logo.png", use_container_width=True)
except FileNotFoundError:
    st.sidebar.warning("Logo não encontrada.")

# Dashboard
st.title("Bem-vindo ao RegeIT!")
st.subheader("Sistema de Gestão de Ativos de TI")
st.markdown("---")

st.write("Adicionar: Animações e Indicadores de Desempenho (KPIs) aparecerão aqui")
