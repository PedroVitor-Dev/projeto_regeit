import streamlit as st
import pandas as pd
from supabase import create_client, Client
from io import BytesIO # Gerando o Excel na memória

#Conexão e Busca
url_supabase = st.secrets["SUPABASE_URL"]
chave_supabase = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url_supabase, chave_supabase)

def buscar_dados():
    #Busca de Ativos
    resposta = supabase.table("equipamentos").select("*").execute()
    return resposta.data

#Interface
st.title("Inventário de Ativos")
st.subheader("Visualize e Gerencie todos os arquivos cadastrados")

dados = buscar_dados()

if not dados:
    st.info("Nenhum equipamento cadastrado ainda.")
else:
    # Cartões de Visualização
    cols = st.columns(3)

    for i, item in enumerate(dados):
        with cols[i % 3]:
            # Essa é a linha que cria a "borda" do cartão e organiza tudo!
            with st.container(border=True):
                st.write(f"### {item['tipo']}")
                
                # Espaço adicionado depois dos dois pontos na Marca
                st.write(f"**Marca:** {item['marca']}")
                
                st.write(f"**Modelo:** {item['modelo']}")
                st.write(f"**S/N:** `{item['numero_serie']}`")
                
                # cor do status
                cor = "green" if item['status'] == "Disponível" else "orange"
                st.markdown(f"**Status:** :{cor}[{item['status']}]")
                
                st.caption(f"📍 {item['localizacao']}")

#Funcionalidade de exportar para Excel
st.markdown("---")
st.write("### 📥 Exportar Dados")

df = pd.DataFrame(dados)

df = df.rename(columns={
        "tipo": "Tipo",
        "marca": "Marca",
        "modelo": "Modelo",
        "numero_serie": "Nº de Série",
        "data_compra": "Data de Compra",
        "status": "Status",
        "localizacao": "Localização",
        "historico": "Histórico",
        "observacoes": "Observações",
        "data_cadastro": "Cadastrado em"
})

#Transformar o Excel para Download
def converter_para_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Equipamentos')
    return output.getvalue()

excel_data = converter_para_excel(df)

#Botão para Download
st.download_button(
        label="📄 Baixar Inventário em Excel",
        data=excel_data,
        file_name="inventario_regeit.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        icon="📥"
    )