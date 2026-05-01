import streamlit as st
import json
import pandas as pd
from streamlit_lottie import st_lottie
from supabase import create_client, Client

# Configuração inicial
st.set_page_config(
    page_title="RegeIT - Gestão de Equipamentos",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
# As três aspas abaixo iniciam o bloco de texto. O Python não vai tentar ler o que está dentro como código lógico.
st.markdown("""
<style>
    /* Importando Fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    /* Forçando a fonte de forma inteligente (sem quebrar ícones) */
    h1, h2, h3, h4, h5, h6, p, a, li, span, div {
        font-family: 'Inter', sans-serif;
    }

    /* Ícones */
    span[class*="material-symbols"], 
    i[class*="material-icons"],
    button[kind="header"] span {
        font-family: 'Material Symbols Rounded', sans-serif !important;
    }

    /* Escondendo o menu padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Métricas */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        padding: 15px 20px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        border-left: 5px solid #0052cc !important; /* Borda lateral azul */
        transition: all 0.3s ease !important; /* Prepara a animação */
    }

    /* Fazer o cartão ficar escuro e visível */
    div[data-testid="stMetric"] * {
        color: #172b4d !important;
    }

    /* Hover */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Containers com borda */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)
# As três aspas acima fecham o bloco de texto com segurança.

# Logo
try:
    st.sidebar.image("logo.png", use_container_width=True)
except FileNotFoundError:
    st.sidebar.warning("Logo não encontrada.")

# Animação
def carregar_lottie_local(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Arquivo {caminho_arquivo} não encontrado!")
        return None 

# Animação de Tecnologia
animacao_ti = carregar_lottie_local("animacao.json")

# Cabeçalho do Painel
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

# Busca de Dados e Conexão
url_supabase = st.secrets["SUPABASE_URL"]
chave_supabase = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url_supabase, chave_supabase)

@st.cache_data(ttl=60)
def buscar_dados_painel():
    resposta = supabase.table("equipamentos").select("*").execute()
    return resposta.data

dados = buscar_dados_painel()

# Gráficos
if not dados:
    st.info("Não há equipamentos cadastrados para gerar estatísticas. Vá até a página de Cadastro!")
else:
    # Dados em tabelas
    df = pd.DataFrame(dados)
    total = len(df)
    disponiveis = len(df[df["status"] == "Disponível"])
    em_uso = len(df[df["status"] == "Em Uso"])
    manutencao = len(df[df["status"] == "Em Manutenção"])

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(label="Total de Ativos 📦", value=total)
    with kpi2:
        st.metric(label="Disponíveis 🟢", value=disponiveis)
    with kpi3:
        st.metric(label="Em Uso 🔵", value=em_uso)
    with kpi4:
        st.metric(label="Em Manutenção 🔴", value=manutencao)

    st.markdown("---")

    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:
        st.write("#### 💻 Quantidade por Tipo de Equipamento")
        contagem_tipos = df["tipo"].value_counts()
        st.bar_chart(contagem_tipos)

    with col_grafico2:
        st.write("#### 🚦 Distribuição por Status")
        contagem_status = df["status"].value_counts()
        st.bar_chart(contagem_status)
        
    if st.button("🔄 Atualizar Painel"):
        buscar_dados_painel.clear()
        st.rerun()