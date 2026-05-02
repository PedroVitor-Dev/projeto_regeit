import streamlit as st
import pandas as pd
import datetime
from supabase import create_client, Client
from io import BytesIO

# Conexão
url_supabase = st.secrets["SUPABASE_URL"]
chave_supabase = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url_supabase, chave_supabase)

@st.cache_data(ttl=60)
def buscar_dados():
    resposta = supabase.table("equipamentos").select("*").execute()
    return resposta.data

if st.button("🔄 Atualizar Tabela"):
    buscar_dados.clear()
    st.rerun()

# Interface
st.title("Inventário de Ativos")
st.subheader("Visualize e Gerencie todos os equipamentos cadastrados")

dados = buscar_dados()

if not dados:
    st.info("Nenhum equipamento cadastrado ainda.")
else:
    df = pd.DataFrame(dados)
    
    with st.container(border=True):
        st.write("🔍 **Busca e Ferramentas**")
        f1, f2, f3 = st.columns([2, 1, 1])

        with f1:
            busca = st.text_input("Pesquisar por Marca, Modelo ou S/N", placeholder="Ex: Dell, HP...")
        with f2:
            lista_tipos = ["Todos"] + sorted(df["tipo"].unique().tolist())
            filtro_tipo = st.selectbox("Filtrar por Tipo", lista_tipos)
        with f3:
            lista_status = ["Todos"] + sorted(df["status"].unique().tolist())
            filtro_status = st.selectbox("Filtrar por Status", lista_status)

        df_filtrado = df.copy()
        
        if busca:
            mask = df_filtrado.apply(lambda row: busca.lower() in str(row['marca']).lower() or 
                                               busca.lower() in str(row['modelo']).lower() or 
                                               busca.lower() in str(row['numero_serie']).lower(), axis=1)
            df_filtrado = df_filtrado[mask]
            
        if filtro_tipo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]
            
        if filtro_status != "Todos":
            df_filtrado = df_filtrado[df_filtrado["status"] == filtro_status]

        st.markdown("---")
        
        # Exportar para Excel
        def converter_para_excel(df_to_export):
            df_formatado = df_to_export.rename(columns={
                "tipo": "Tipo", "marca": "Marca", "modelo": "Modelo",
                "numero_serie": "Nº de Série", "data_compra": "Data de Compra",
                "status": "Status", "localizacao": "Localização",
                "historico": "Histórico", "observacoes": "Observações",
                "data_cadastro": "Cadastrado em"
            })
            if "id" in df_formatado.columns:
                df_formatado = df_formatado.drop(columns=["id"])
                
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
            use_container_width=True
        )

    st.write(f"Exibindo **{len(df_filtrado)}** equipamentos:")
    
    if df_filtrado.empty:
        st.warning("Nenhum resultado encontrado para os filtros selecionados.")
    else:
        dados_finais = df_filtrado.to_dict('records')
        cols = st.columns(3)

        for i, item in enumerate(dados_finais):
            with cols[i % 3]:
                with st.container(border=True):
                    st.write(f"### {item['tipo']}")
                    st.write(f"**Marca:** {item['marca']}")
                    st.write(f"**Modelo:** {item['modelo']}")
                    st.write(f"**S/N:** `{item['numero_serie']}`")
                    
                    cor = "green" if item['status'] == "Disponível" else "orange" if item['status'] == "Em Uso" else "red"
                    st.markdown(f"**Status:** :{cor}[{item['status']}]")
                    st.caption(f"📍 {item.get('localizacao', 'Não informada')}")

        # Gerenciamento
        st.markdown("---")
        st.subheader("⚙️ Gerenciar Equipamento")
        
        mapa_equipamentos = {f"{item['marca']} {item['modelo']} (S/N: {item['numero_serie']})": item for item in dados_finais}
        
        escolha_str = st.selectbox("Selecione o equipamento que deseja modificar:", list(mapa_equipamentos.keys()))
        item_selecionado = mapa_equipamentos[escolha_str]

        aba_editar, aba_excluir = st.tabs(["✏️ Editar Dados", "🗑️ Excluir Equipamento"])

        with aba_editar:
            with st.form("form_editar"):
                col1, col2 = st.columns(2)
                
                with col1:
                    novo_tipo = st.text_input("Tipo", value=item_selecionado.get("tipo", ""))
                    nova_marca = st.text_input("Marca", value=item_selecionado.get("marca", ""))
                    novo_modelo = st.text_input("Modelo", value=item_selecionado.get("modelo", ""))
                    novo_sn = st.text_input("Nº de Série", value=item_selecionado.get("numero_serie", ""))
                
                with col2:
                    data_str = item_selecionado.get("data_compra")
                    try:
                        data_atual = datetime.datetime.strptime(str(data_str), "%Y-%m-%d").date()
                    except:
                        data_atual = datetime.date.today()
                        
                    nova_data = st.date_input("Data de Compra", value=data_atual)
                    
                    lista_status_opcoes = ["Disponível", "Em Uso", "Em Manutenção", "Descartado"]
                    status_atual = item_selecionado.get("status", "Disponível")
                    
                    if status_atual not in lista_status_opcoes:
                        lista_status_opcoes.append(status_atual)
                        
                    novo_status = st.selectbox("Status", lista_status_opcoes, index=lista_status_opcoes.index(status_atual))
                    nova_localizacao = st.text_input("Localização", value=item_selecionado.get("localizacao", ""))
                
                novas_observacoes = st.text_area("Observações", value=item_selecionado.get("observacoes", ""))

                #Auditoria de histórico
                st.write("---")
                st.write("🔒 **Histórico de Alterações (Somente Leitura)**")
                historico_antigo = item_selecionado.get("historico", "")
                
                if historico_antigo:
                    st.info(historico_antigo)
                else:
                    st.caption("Nenhum histórico registrado para este equipamento.")

                #Campo em branco para notas
                nota_manual = st.text_area("Adicionar nova nota ao histórico (Opcional)", placeholder="Digite aqui uma ocorrência, defeito, ou observação...")
                # ----------------------------------------------

                botao_salvar = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)

                if botao_salvar:
                    #Base do histórico protegida
                    historico_final = historico_antigo
                    data_hora_agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    
                    #Nota manual
                    if nota_manual.strip():
                        texto_nota = f"\n[{data_hora_agora}] Observação: {nota_manual.strip()}"
                        if historico_final:
                            historico_final = historico_final + texto_nota
                        else:
                            historico_final = texto_nota.strip()
                    
                    #Nota em caso do texto alterado
                    if status_atual != novo_status:
                        texto_status = f"\n[{data_hora_agora}] Status alterado de '{status_atual}' para '{novo_status}'."
                        if historico_final:
                            historico_final = historico_final + texto_status
                        else:
                            historico_final = texto_status.strip()

                    try:
                        supabase.table("equipamentos").update({
                            "tipo": novo_tipo,
                            "marca": nova_marca,
                            "modelo": novo_modelo,
                            "numero_serie": novo_sn,
                            "data_compra": str(nova_data),
                            "status": novo_status,
                            "localizacao": nova_localizacao,
                            "historico": historico_final, # Salva o histórico combinado e protegido
                            "observacoes": novas_observacoes
                        }).eq("id", item_selecionado["id"]).execute()
                        
                        st.success("Equipamento atualizado com sucesso!")
                        buscar_dados.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {e}")

        # Local para Excluir
        with aba_excluir:
            st.warning(f"⚠️ Atenção: Esta ação irá apagar o equipamento **{item_selecionado['marca']} {item_selecionado['modelo']}** permanentemente.")
            
            if st.button("🗑️ Confirmar Exclusão", type="primary"):
                try:
                    supabase.table("equipamentos").delete().eq("id", item_selecionado["id"]).execute()
                    st.success("Equipamento excluído com sucesso!")
                    buscar_dados.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {e}")