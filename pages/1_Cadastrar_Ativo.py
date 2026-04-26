import streamlit as st

st.title("Cadastrar Novo Ativo")
st.subheader("Adicione um novo equipamento ao sistema")

#Formulário
with st.form(key="form_cadastro_ativo"):

    #Colunas
    col1, col2 = st.columns(2)

    #Primeira coluna da esquerda
    with col1:
        tipo = st.selectbox("Tipo de Equipamento", ["Notebook", "Desktop", "Monitor", "Smartphone", "Impressora", "Servidor", "Outros"])
        marca = st.text_input("Marca")
        modelo = st.text_input("Modelo")
        numero_serie = st.text_input("Número de Série")

    #Segunda coluna da direita
    with col2:
        data_compra = st.date_input("Data de Compra")
        status = st.selectbox("Status do Equipamento", ["Disponível", "Em Uso", "Em Manutenção", "Descartado"])
        localizacao = st.text_input("Localização (Ex. Setor de Vendas, Almoxarifado, Etc...)")

    #Campos fora do coluna
    st.markdown("---")
    historico = st.text_area("Histórico de Equipamento")
    observacoes = st.text_area("Observações Adicionais")

    #Botão de Enviar
    botao_salvar = st.form_submit_button("Salvar Equipamento")

if botao_salvar:
    st.success(f"Sucesso! O {tipo} da marca {marca} foi registrado.")
    st.info(f"Número de Série Registrado: {numero_serie} | Status: {status}")