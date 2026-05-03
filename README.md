# RegeIT - Sistema de Gestão de Ativos de TI 💻

## 📖 Sobre o Projeto
O **RegeIT** é uma aplicação web moderna e interativa desenvolvida para facilitar e centralizar a gestão de equipamentos de Tecnologia da Informação. O objetivo principal é oferecer controle total sobre o ciclo de vida dos ativos da empresa, desde a aquisição até o descarte, garantindo rastreabilidade, segurança e fácil acesso às informações.

## 🚀 Funcionalidades Principais

O sistema é dividido em três módulos inteligentes:

### 📊 1. Painel de Controle (Dashboard)
* **Visão Geral em Tempo Real:** Indicadores (KPIs) mostrando o total de ativos e a contagem exata de equipamentos Disponíveis, Em Uso e Em Manutenção.
* **Gráficos Dinâmicos:** Visualização rápida da quantidade de equipamentos por tipo e distribuição por status de uso.
* **Interface Responsiva:** Design otimizado com feedback visual de carregamento e adaptação perfeita a temas claros e escuros (Dark Mode).

### ➕ 2. Cadastro de Ativos
* **Formulário Padronizado:** Inserção de novos equipamentos com campos detalhados (Tipo, Marca, Modelo, Número de Série, Data de Compra, Localização e Observações).
* **Auditoria Automática (Ponto Zero):** O sistema gera automaticamente um registro de histórico seguro, contendo a data, a hora e o status inicial do ativo no exato momento do cadastro.
* **Interface Focada:** Prevenção contra preenchimento automático do navegador nos campos de texto para evitar erros e poluição visual.

### 📋 3. Listagem e Gerenciamento
* **Visualização Avançada:** Disposição dos dados em formato de cartões (cards) para rápida identificação visual das características e localização do ativo.
* **Filtros e Busca Inteligente:** Pesquisa instantânea por texto (Marca, Modelo ou S/N) combinada com filtros em cascata por categorias (Tipo e Status).
* **Exportação de Dados:** Capacidade de gerar e baixar planilhas do Microsoft Excel (`.xlsx`) com base nos filtros selecionados em tela.
* **Edição de Dados Inteligente:** Formulário dinâmico para atualização de informações cadastrais.
* **Trilha de Auditoria Inviolável:** Um histórico de alterações com permissão de "Somente Leitura". Qualquer mudança de status gera uma nota automática com carimbo de tempo. O usuário também pode apensar novas observações de ocorrências de forma segura, sem alterar o passado.
* **Exclusão de Registros:** Mecanismo integrado e seguro para remover equipamentos permanentemente do banco de dados.

## 🛠️ Tecnologias Utilizadas
* **Python:** Linguagem base de toda a lógica do servidor.
* **Streamlit:** Framework utilizado para a criação da interface web e componentes interativos.
* **Pandas:** Biblioteca para manipulação avançada, filtragem e estruturação de dados em formato tabular.
* **Supabase:** Banco de dados relacional em nuvem, moderno e operando em tempo real.

## 🚧 Status do Projeto
**Status: Em Produção (Em Desenvolvimento) ⚙️**
O RegeIT encontra-se atualmente em fase de desenvolvimento ativo. Novas funcionalidades, otimizações de código e refinamentos de interface estão sendo planejados e implementados continuamente para garantir a máxima eficiência na gestão de inventário.
