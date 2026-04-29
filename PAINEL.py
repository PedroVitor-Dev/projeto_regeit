import streamlit as st
import json
from streamlit_lottie import st_lottie

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
#Animação
def carregar_lottie_local(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Arquivo {caminho_arquivo} não encontrado!")
        return None 

# Animação de Tecnologia
animacao_ti = carregar_lottie_local("animacao.json")

#Cabeçalho do Painel
col1, col2 = st.columns([2, 1])

# Dashboard
with col1:
    st.title("Bem-vindo ao RegeIT!")
    st.subheader("Sistema de Gestão de Ativos de TI")
    st.write("Acompanhe, gerencie e tenha controle total sobre todos os equipamentos em um só lugar.")

with col2:
    if animacao_ti:
        st_lottie(animacao_ti, height=200, key="animacao_inicial")

st.markdown("---")

st.write("### 📊 Visão Geral do Sistema")
st.write("Adicionar: Indicadores de Desempenho (KPIs) aparecerão aqui")
