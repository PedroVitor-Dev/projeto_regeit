import streamlit as st
import pandas as pd
from supabase import create_client, Client
from io import BytesIO # Gerando o Excel na memória

#Conexão e Busca
url_supabase = st.secrets["SUPABASE_URL"]
chave_supabase = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url_supabase, chave_supabase)

#Configuração de Cache
@st.cache_data(ttl=60)
def buscar_dados():
    resposta = supabase.table("equipamentos").select("*").execute()
    return resposta.data
if st.button("🔄 Atualizar Tabela"):
    buscar_dados.clear()
    st.rerun() #Recarregar

#Interface
st.title("Inventário de Ativos")
st.subheader("Visualize e Gerencie todos os arquivos cadastrados")

dados = buscar_dados()

if not dados:
    st.info("Nenhum equipamento cadastrado ainda.")
else:
    # Dataframe para facilitar filtros
    df = pd.DataFrame(dados)
    #Filtros e Exportação
    with st.container(border=True):
        st.write("🔍 **Busca e Ferramentas**")

        f1,f2, f3 = st.columns([2, 1, 1])

        with f1:
            busca = st.text_input("Pesquisar por Marca, Modelo ou S/N", placeholder="Ex: Dell, HP...")
        with f2:
            lista_tipos = ["Todos"] + sorted(df["tipo"].unique().tolist())
            filtro_tipo = st.selectbox("Filtrar por Tipo", lista_tipos)
        with  f3:
            lista_status = ["Todos"] + sorted(df["status"].unique().tolist())
            filtro_status = st.selectbox("Filtrar por Status", lista_status)

        #Filtragem no Pandas
        df_filtrado = df.copy()
        
        if busca:
            # Procura o termo na marca, modelo ou número de série (sem ligar para maiúsculas)
            mask = df_filtrado.apply(lambda row: busca.lower() in str(row['marca']).lower() or 
                                               busca.lower() in str(row['modelo']).lower() or 
                                               busca.lower() in str(row['numero_serie']).lower(), axis=1)
            df_filtrado = df_filtrado[mask]
            
        if filtro_tipo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]
            
        if filtro_status != "Todos":
            df_filtrado = df_filtrado[df_filtrado["status"] == filtro_status]

        # Botão de exportar o que está sendo filtrado
        st.markdown("---")
        
        def converter_para_excel(df_to_export):
            # Limpamos os nomes das colunas para o Excel
            df_formatado = df_to_export.rename(columns={
                "tipo": "Tipo", "marca": "Marca", "modelo": "Modelo",
                "numero_serie": "Nº de Série", "data_compra": "Data de Compra",
                "status": "Status", "localizacao": "Localização",
                "historico": "Histórico", "observacoes": "Observações",
                "data_cadastro": "Cadastrado em"
            })
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_formatado.to_excel(writer, index=False, sheet_name='Equipamentos')
            return output.getvalue()

        excel_data = converter_para_excel(df_filtrado)

        st.download_button(
            label="📄 Exportar estes resultados para Excel",
            data=excel_data,
            file_name="inventario_filtrado_regeit.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            icon="📥",
            use_container_width=True # Botão ocupa a largura toda para ficar fácil de clicar
        )

    # Cartões Filtrados

    st.write(f"Exibindo **{len(df_filtrado)}** equipamentos:")
    
    if df_filtrado.empty:
        st.warning("Nenhum resultado encontrado para os filtros selecionados.")
    else:
        # Criamos o grid de cartões
        dados_finais = df_filtrado.to_dict('records')
        cols = st.columns(3)

        for i, item in enumerate(dados_finais):
            with cols[i % 3]:
                with st.container(border=True):
                    st.write(f"### {item['tipo']}")
                    st.write(f"**Marca:** {item['marca']}")
                    st.write(f"**Modelo:** {item['modelo']}")
                    st.write(f"**S/N:** `{item['numero_serie']}`")
                    
                    cor = "green" if item['status'] == "Disponível" else "orange"
                    st.markdown(f"**Status:** :{cor}[{item['status']}]")
                    
                    st.caption(f"📍 {item['localizacao']}")