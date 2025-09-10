# 📊 Dashboard de Vendas

Este projeto é uma aplicação interativa desenvolvida com [Streamlit](https://streamlit.io/) para análise de dados de vendas.  
O objetivo é oferecer uma visualização clara e dinâmica do desempenho da empresa ao longo dos anos, com métricas financeiras, filtros customizados e gráficos interativos.

---

## ⚙️ Funcionalidades

- 🔎 **Filtros dinâmicos**
  - Seleção por **região** e **ano**

- 💰 **Métricas principais**
  - Lucro total por ano e variação em relação ao ano anterior
  - Vendas totais e quantidade de pedidos

- 📈 **Visualizações**
  - Gráfico de linha com evolução anual
  - Gráfico de barras para os produtos mais vendidos
  - Mapa geográfico (scatter_geo) mostrando desempenho por estado
  - Tabelas dinâmicas com filtros aplicáveis

---

## 📂 Estrutura do projeto

dashboard_vendas/

│── Dashboard.py # Arquivo principal da aplicação

│── pages/ # Páginas adicionais (Dados brutos)

│── data/ # Arquivos CSV com os dados de vendas

│── venv/ # Ambiente virtual

│── .streamlit/

│ └── config.toml # Configurações de tema

│── requirements.txt # Dependências do projeto

---

## 🚀 Como executar

1. Clone este repositório:

git clone https://github.com/seu-usuario/dashboard_vendas.git

cd dashboard_vendas


2. Crie e ative um ambiente virtual (opcional, mas recomendado):

python -m venv venv

source venv/bin/activate   # Linux/Mac

venv\Scripts\activate      # Windows


3. Instale as dependências:

pip install -r requirements.txt


4. Rode a aplicação:

streamlit run Dashboard.py


🛠️ Tecnologias utilizadas

- Python
- Pandas
- Plotly
- Streamlit

✨ Autor

Desenvolvido por Luis Guilherme

🌐 https://www.linkedin.com/in/lu%C3%ADs-ferreira-218205175/


