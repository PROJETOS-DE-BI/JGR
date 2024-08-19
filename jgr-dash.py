import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image  # Se a imagem estiver em um formato suportado pelo Pillow
import base64
from io import BytesIO

## Função para converter a imagem em base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Carrega a imagem
imagem = Image.open(r"C:\Users\gusta\Desktop\JGR\foto_streamlit3.png")  # Substitua pelo caminho da sua imagem

# Custom CSS para a faixa com gradiente e imagem sobreposta
st.markdown(
    """
    <style>
    .full-width-banner {
        position: relative;
        width: 100%;
        height: 200px;  /* Ajuste a altura conforme necessário */
        background: linear-gradient(90deg, blue, white);
        display: flex;
        align-items: center;
        padding: 20px;
        box-sizing: border-box;
    }
    .text-container {
        text-align: center;
        color: black;
        flex: 1;
        z-index: 1;  /* Garante que o texto fique acima da imagem */
    }
    .text-container h1 {
        font-size: 36px;
        margin: 0;
    }
    .text-container p {
        font-size: 18px;
        margin: 0;
    }
    .full-width-banner img {
        position: absolute;
        top: 20px;  /* Posição vertical da imagem */
        left: 20px;  /* Ajuste a posição horizontal da imagem para alinhar com o padding */
        height: 150px;  /* Ajuste a altura da imagem conforme necessário */
        z-index: 0;  /* Garante que a imagem fique atrás do texto */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuração da página com a faixa ocupando toda a largura
st.markdown(
    """
    <div class="full-width-banner">
        <img src="data:image/png;base64,{}" alt="logo">
        <div class="text-container">
            <h1>Dashboard de Contratos</h1>
            <p>Informações sobre os contratos fechados pela JGR em 2024</p>
        </div>
    </div>
    """.format(image_to_base64(imagem)),
    unsafe_allow_html=True
)

# Função para carregar os dados com caching
@st.cache_data
def carregar_dados():
    tabela = pd.read_csv(r"C:\Users\gusta\Desktop\JGR\contrato.csv")
    return tabela

with st.container():
    st.write("---")


# Carrega os dados
dados = carregar_dados()

# Certifique-se de que a coluna 'data' está no formato datetime
dados['data'] = pd.to_datetime(dados['data'], format='%d/%m/%Y', errors='coerce')

# Cria uma nova variável "total"
dados['total'] = dados['qtde_h'] * dados['vlr_h']

# Adiciona uma coluna com o mês e ano
dados['mes'] = dados['data'].dt.to_period('M').astype(str)

# Agrega os dados por mês para o gráfico de barras
dados_mensal_barras = dados.groupby('mes')['qtde_h'].sum().reset_index()

# Agrega os dados por mês para o gráfico de linhas
dados_mensal_linhas = dados.groupby('mes')['total'].sum().reset_index()

# Calcula a média para cada gráfico e arredonda
media_valor = round(dados_mensal_barras['qtde_h'].mean(), 0)
media_total = f"R$ {round(dados_mensal_linhas['total'].mean(), 2):,.2f}"


# Criação do gráfico de barras com Plotly
fig_barras = px.bar(dados_mensal_barras, x='mes', y='qtde_h', title='Quantidade de Contratos',
                    labels={'mes': 'Mês', 'qtde_h': 'Quantidade'})

# Adiciona a linha de média no gráfico de barras
fig_barras.add_trace(
    go.Scatter(
        x=dados_mensal_barras['mes'],
        y=[media_valor] * len(dados_mensal_barras),
        mode='lines',
        name='Média',
        line=dict(color='red', dash='dash')
    )
)

# Criação do gráfico de linhas com marcadores (bolinhas) com Plotly
fig_linhas = go.Figure(go.Scatter(
    x=dados_mensal_linhas['mes'],
    y=dados_mensal_linhas['total'],
    mode='lines+markers',
    name='Total de "Total" por Mês',  # Nome da linha principal na legenda
    showlegend=False  # Não mostra a linha principal na legenda
))

# Adiciona a linha de média no gráfico de linhas
fig_linhas.add_trace(
    go.Scatter(
        x=dados_mensal_linhas['mes'],
        y=[float(media_total.replace('R$', '').replace(',', ''))] * len(dados_mensal_linhas),
        mode='lines',
        name='Média',
        line=dict(color='red', dash='dash')
    )
)

# Atualiza o layout do gráfico de linhas
fig_linhas.update_layout(
    title='Recebimentos de Contratos em 2024',  # Título do gráfico de linhas
    yaxis_tickprefix='R$ ',
    yaxis_tickformat=',.2f',
    autosize=True
)


# Exibe os gráficos lado a lado com proporções definidas
col1, col2 = st.columns([2, 2])
with col1:
    st.plotly_chart(fig_barras, use_container_width=True)
with col2:
    st.plotly_chart(fig_linhas, use_container_width=True)

