import streamlit as st
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon='✅')
    time.sleep(5)
    sucesso.empty()

st.title('DADOS BRUTOS')

dados = pd.read_csv('./data/relatorio_vendas.csv')

dados['data_pedido'] = pd.to_datetime(dados['data_pedido'], format='%Y-%m-%d')
dados['data_envio'] = pd.to_datetime(dados['data_envio'], format='%Y-%m-%d')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Data do pedido'):
    data_pedido = st.date_input('Selecione a data do pedido', (dados['data_pedido'].min(), dados['data_pedido'].max()))
with st.sidebar.expander('Data do envio'):
    data_envio = st.date_input('Selecione a data do envio', (dados['data_envio'].min(), dados['data_envio'].max()))
with st.sidebar.expander('Modo de envio'):
    modo_envio = st.multiselect('Selecione o modo de envio', dados['modo_envio'].unique(), dados['modo_envio'].unique())
with st.sidebar.expander('Nome do cliente'):
    nome_cliente = st.multiselect('Selecione o nome do cliente', dados['nome_cliente'].unique(), dados['nome_cliente'].unique())
with st.sidebar.expander('Segmento do cliente'):
    segmento_cliente = st.multiselect('Selecione o segmento do cliente', dados['segmento_cliente'].unique(), dados['segmento_cliente'].unique())
with st.sidebar.expander('Cidade'):
    cidade = st.multiselect('Selecione a cidade', dados['cidade'].unique(), dados['cidade'].unique())
with st.sidebar.expander('Estado'):
    estado = st.multiselect('Selecione o estado', dados['estado'].unique(), dados['estado'].unique())  
with st.sidebar.expander('Região'):
    regiao = st.multiselect('Selecione a região', dados['regiao'].unique(), dados['regiao'].unique())
with st.sidebar.expander('Departamento'):
    departamento = st.multiselect('Selecione o departamento', dados['departamento'].unique(), dados['departamento'].unique())
with st.sidebar.expander('Tipo de produto'):
    produto = st.multiselect('Selecione o tipo do produto', dados['tipo_produto'].unique(), dados['tipo_produto'].unique())
with st.sidebar.expander('Preço base'):
    preco_base = st.slider('Selecione o preço base', 0, 9100, (0, 9100))
with st.sidebar.expander('Preço unitário de venda'):
    preco_venda = st.slider('Selecione o preço unitário', 0, 12000, (0, 12000))
with st.sidebar.expander('Quantidade'):
    quantidade = st.slider('Selecione a quantidade', 0, 14, (0, 14))
with st.sidebar.expander('Receita de vendas'):
    receita = st.slider('Selecione a receita de vendas', 0, 60000, (0, 60000))
with st.sidebar.expander('Lucro'):
    lucro = st.slider('Selecione o lucro', -11220, 14280, (-11220, 14280))

query = '''
@data_pedido[0] <= data_pedido <= @data_pedido[1] and \
@data_envio[0] <= data_envio <= @data_envio[1] and \
modo_envio in @modo_envio and \
nome_cliente in @nome_cliente and \
segmento_cliente in @segmento_cliente and \
cidade in @cidade and \
estado in @estado and \
regiao in @regiao and \
departamento in @departamento and \
tipo_produto in @produto and \
@preco_base[0] <= preco_base <= @preco_base[1] and \
@preco_venda[0] <= preco_unit_venda <= @preco_venda[1] and \
@quantidade[0] <= quantidade <= @quantidade[1] and \
@receita[0] <= vendas <= @receita[1] and \
@lucro[0] <= lucro <= @lucro[1]
'''
dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Escreva um nome para o arquivo')
col1, col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'
with col2:
    st.download_button('Fazer o download da tabela em csv', data=converte_csv(dados_filtrados), file_name=nome_arquivo, mime='text/csv', on_click=mensagem_sucesso)