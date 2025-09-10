import streamlit as st
import pandas as pd
import plotly.express as px

# Definindo latitude e longitude
coords_estados = {
    "Acre": {"lat": -9.0238, "lon": -70.8120},
    "Alagoas": {"lat": -9.5713, "lon": -36.7820},
    "Amapá": {"lat":  1.4142, "lon": -51.6035},
    "Amazonas": {"lat": -3.4168, "lon": -65.8561},
    "Bahia": {"lat": -12.9714, "lon": -41.4822},
    "Ceará": {"lat": -5.4984, "lon": -39.3206},
    "Distrito Federal": {"lat": -15.8267, "lon": -47.9218},
    "Espírito Santo": {"lat": -19.1834, "lon": -40.3089},
    "Goiás": {"lat": -15.8270, "lon": -49.8362},
    "Maranhão": {"lat": -4.9609, "lon": -45.2744},
    "Mato Grosso": {"lat": -12.6819, "lon": -56.9211},
    "Mato Grosso do Sul": {"lat": -20.7722, "lon": -54.7852},
    "Minas Gerais": {"lat": -18.5122, "lon": -44.5550},
    "Pará": {"lat": -3.4168, "lon": -52.1416},
    "Paraíba": {"lat": -7.2399, "lon": -36.7819},
    "Paraná": {"lat": -24.8947, "lon": -51.5546},
    "Pernambuco": {"lat": -8.8137, "lon": -36.9541},
    "Piauí": {"lat": -7.7183, "lon": -42.7289},
    "Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729},
    "Rio Grande do Norte": {"lat": -5.4026, "lon": -36.9541},
    "Rio Grande do Sul": {"lat": -30.0346, "lon": -52.9530},
    "Rondônia": {"lat": -10.8264, "lon": -63.2990},
    "Roraima": {"lat":  2.7376, "lon": -62.0751},
    "Santa Catarina": {"lat": -27.2423, "lon": -50.2189},
    "São Paulo": {"lat": -22.9083, "lon": -48.4467},
    "Sergipe": {"lat": -10.5741, "lon": -37.3857},
    "Tocantins": {"lat": -10.1753, "lon": -48.2982}
}

# Paleta de cores
AZUL1, AZUL2, AZUL3, AZUL4, AZUL5 = '#03045e', '#0077b6', "#00b4d8", '#90e0ef', '#CDDBF3'
CINZA1, CINZA2, CINZA3, CINZA4, CINZA5 = '#212529', '#495057', '#adb5bd', '#dee2e6', '#f8f9fa'
VERMELHO1, LARANJA1, AMARELO1, VERDE1, VERDE2 = "#f83504", '#f4a261',	"#f7d172", '#4c956c', '#2a9d8f'

# Função para formatação dos valores em mil/milhões
def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

st.set_page_config(layout='wide')

st.title('DASHBOARD VENDAS - LOJA DE DEPARTAMENTO 🛒')

# Filtros
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']

st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)

if regiao == 'Brasil':
    regiao = ''

todos_anos = st.sidebar.checkbox('Dados de todos o período', value=True)
if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2016, 2019)

# Importando dados
dados = pd.read_csv('./data/relatorio_vendas.csv')

# Transformação das colunas com data para datetime
dados['data_pedido'] = pd.to_datetime(dados['data_pedido'], format='%Y-%m-%d')
dados['data_envio'] = pd.to_datetime(dados['data_envio'], format='%Y-%m-%d')

# Filtrar região se selecionada
if regiao:
    dados = dados[dados['regiao'].str.lower() == regiao.lower()]

# Filtrar ano se selecionado
if ano:
    dados = dados[dados['data_pedido'].dt.year == ano]

# Criando colunas lat e lon
dados['lat'] = dados['estado'].map(lambda x: coords_estados[x]['lat'])
dados['lon'] = dados['estado'].map(lambda x: coords_estados[x]['lon'])

# Função para calcular métricas no dashboard
def calcular_metricas(dados, coluna_valor, ano_filtro=None):
    df_temp = dados.copy()
    df_temp['ano'] = df_temp['data_pedido'].dt.year

    if ano_filtro is not None:
        df_temp = df_temp[df_temp['ano'] == ano_filtro]

    df_ano = df_temp.groupby('ano')[[coluna_valor]].sum().sort_index()
    if df_ano.empty:
        return None, None, None
    ultimo_ano = df_ano.index[-1]
    valor_ultimo_ano = df_ano.iloc[-1,0]

    if len(df_ano) > 1:
        delta = df_ano.iloc[-1,0] - df_ano.iloc[-2,0]
    else:
        delta = None
    return ultimo_ano, valor_ultimo_ano, delta    

# Definição das variáveis para métricas
if todos_anos:
    ano_filtro = None
else:
    ano_filtro = ano
ultimo_ano, lucro_final, delta_lucro = calcular_metricas(dados, 'lucro', ano_filtro)
ultimo_ano, vendas_final, delta_vendas = calcular_metricas(dados, 'vendas', ano_filtro)

# Tabela 1 - Receita por mês
receita_mensal = dados.set_index('data_pedido').groupby(pd.Grouper(freq='ME'))['vendas'].sum().reset_index()
receita_mensal['ano'] = receita_mensal['data_pedido'].dt.year
meses = {1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun", 
         7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"}
receita_mensal['mes'] = receita_mensal['data_pedido'].dt.month.map(meses)

# Tabela 2 - Vendas por ano
receita_ano = receita_mensal.groupby('ano')[['vendas']].sum()
receita_ano['vendas'] = round(receita_ano['vendas']/1e6, 2)

# Tabela 3 - Faturamento produtos
fat_prod = dados.groupby('tipo_produto')[['vendas']].sum().sort_values('vendas', ascending=True)
fat_prod = fat_prod.tail(10)
fat_prod = round(fat_prod['vendas']/1000,2)

# Tabela 4 - Faturamento por estado
fat_estados = dados.groupby('estado')[['vendas']].sum()
fat_estados = dados.drop_duplicates(subset='estado')[['estado', 'lat', 'lon']].merge(fat_estados, 
                                                                                     left_on='estado', 
                                                                                     right_index=True).sort_values('vendas', 
                                                                                                                   ascending=False)

# Visualização tabela 1
fig_receita_mensal = px.line(receita_mensal, 
                             x='mes',
                             y='vendas',
                             markers=True,
                             range_y=(0, receita_mensal.max()),
                             color='ano',
                             line_dash='ano',
                             title='Receita total mensal',
                             labels={'vendas':'Receita (R$)', 'mes':'Mês', 'ano':'Ano'},
                             color_discrete_sequence=(AZUL2, VERMELHO1, LARANJA1, VERDE2))
fig_receita_mensal.update_layout(yaxis_title='',
                                 xaxis_title='')
fig_receita_mensal.update_xaxes(tickfont=dict(size=14))
fig_receita_mensal.update_yaxes(tickfont=dict(size=14))

# Visualização tabela 2
fig_receita_ano = px.bar(receita_ano,
                         x=receita_ano.index,
                         y='vendas',
                         text_auto=True,
                         title='Receita total anual',
                         labels={'vendas':'Receita (em milhões R$)', 'ano':'Ano'},
                         range_y=(0, 2.5),
                         color_discrete_sequence=[AZUL2])
fig_receita_ano.update_layout(yaxis_title='',
                              xaxis_title='',
                              showlegend=False)
fig_receita_ano.update_xaxes(type='category', tickfont=dict(size=14))
fig_receita_ano.update_yaxes(showticklabels=False, showgrid=False)
fig_receita_ano.update_traces(texttemplate='R$ %{y} milhões', textposition='outside', textfont=dict(size=14))

# Visualização tabela 3
fig_fat_prod = px.bar(fat_prod, x='vendas', y=fat_prod.index,
                      text_auto=True,
                      title='Faturamento por produtos',
                      labels={'vendas':'Receita (em R$)', 'y':'Tipo do produto'},
                      color_discrete_sequence=[AZUL2])
fig_fat_prod.update_layout(yaxis_title='',
                           xaxis_title='',
                           showlegend=False)
fig_fat_prod.update_xaxes(tickfont=dict(size=14), showticklabels=False)
fig_fat_prod.update_traces(texttemplate='R$ %{x} mil', textposition='inside', textfont=dict(size=16))

# Visualização tabela 4
fig_mapa_vendas = px.scatter_geo(fat_estados, 
                                 lat='lat', 
                                 lon='lon',
                                 scope='south america',
                                 size='vendas',
                                 template='seaborn',
                                 hover_name='estado',
                                 hover_data={'lat':False, 'lon':False},
                                 title='Faturamento por estado',
                                 labels={'vendas':'Receita (em R$)'})
fig_mapa_vendas.update_layout(template="plotly_dark", geo=dict(bgcolor="rgba(0,0,0,0)", 
                                                               lakecolor="rgba(0,0,0,0)",  
                                                               landcolor="rgba(0,0,0,0)"))

col1, col2 = st.columns(2)
with col1:
    st.metric('Receita total', formata_numero(dados['vendas'].sum()))    
    if ultimo_ano is not None:
        st.metric(
            label=f'Lucro em {ultimo_ano}',
            value=f'R$ {formata_numero(lucro_final)}',
            delta=f'R$ {formata_numero(delta_lucro)}' if delta_lucro is not None else None)
    else:
        st.warning('Não há dados disponíveis para o filtro selecionado')
    st.plotly_chart(fig_receita_ano, use_container_width=True)
    st.plotly_chart(fig_fat_prod, use_container_width=True)
with col2:
    st.metric('Quantidade de vendas total', formata_numero(dados.shape[0]))
    if ultimo_ano is not None:
        st.metric(
            label=f'Receita em {ultimo_ano}',
            value=f'R$ {formata_numero(vendas_final)}',
            delta=f'R$ {formata_numero(delta_vendas)}' if delta_vendas is not None else None)    
    st.plotly_chart(fig_receita_mensal, use_container_width=True)
    st.plotly_chart(fig_mapa_vendas, use_container_width=True)
    