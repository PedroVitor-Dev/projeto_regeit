import streamlit as st
import datetime #Para aumentar os limites de data.
from supabase import create_client, Client # Base do Supabase

# Conexão com o banco de dados
#chaves no arquivo secrets.toml
url_supabase = st.secrets["SUPABASE_URL"]
chave_supabase = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url_supabase, chave_supabase)

#Início do Front
st.title("Cadastrar Novo Ativo")
st.subheader("Adicione um novo equipamento ao sistema")

#Formulário
with st.form(key="form_cadastro_ativo", enter_to_submit=False, clear_on_submit=True):

    #Colunas
    col1, col2 = st.columns(2)

    #Primeira coluna da esquerda
    with col1:
        tipo = st.selectbox("Tipo de Equipamento", ["Notebook", "Desktop", "Monitor", "Smartphone", "Impressora", "Servidor", "Outros"])
        marca = st.text_input("Marca", autocomplete="off")
        modelo = st.text_input("Modelo", autocomplete="off")
        numero_serie = st.text_input("Número de Série", autocomplete="off")

    #Segunda coluna da direita
    with col2:
        data_minima = datetime.date(2000, 1, 1)
        data_maxima = datetime.date(2050,12, 31)

        data_compra = st.date_input(
            "Data de Compra",
            format="DD/MM/YYYY",
            min_value=data_minima,
            max_value=data_maxima
        )
        status = st.selectbox("Status do Equipamento", ["Disponível", "Em Uso", "Em Manutenção", "Descartado"])
        localizacao = st.text_input("Localização (Ex. Setor de Vendas, Almoxarifado, Etc...)")

    #Campos fora do coluna
    st.markdown("---")
    
    # --- NOVO COMENTÁRIO: O campo de histórico manual foi removido daqui! ---
    
    observacoes = st.text_area("Observações Adicionais")

    #Botão de Enviar
    botao_salvar = st.form_submit_button("Salvar Equipamento")

if botao_salvar:
    
    #Primeira linha para o log de alteracoes
    data_hora_agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    historico_inicial = f"[{data_hora_agora}] Equipamento cadastrado no sistema com status '{status}'."

#Lógica de Envio
    dados_do_ativo = {
        "tipo": tipo,
        "marca": marca,
        "modelo": modelo,
        "numero_serie": numero_serie,
        "data_compra": str(data_compra),
        "status": status,
        "localizacao": localizacao,
        "historico": historico_inicial, # Passamos a variável automática para o banco
        "observacoes": observacoes
    }
#Caso Offline
    try:
        resposta = supabase.table("equipamentos").insert(dados_do_ativo).execute()

        st.success(f"Sucesso! O {tipo} da marca {marca} foi salvo no banco de dados.")
        st.toast("Equipamento salvo com sucesso!", icon="💾") #Comemoração!
    except Exception as erro:
        st.error(f"Ops! Ocorreu um erro ao salvar o banco de dados: {erro}")