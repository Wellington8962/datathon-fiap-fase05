import streamlit as st
from util.layout import output_layout
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Datathon | Fase 5 | FIAP", layout='wide')
output_layout()

st.header(':blue[FIAP PÓS TECH – DATA ANALYTICS, 2024]',divider="orange")

st.subheader(':orange[Datathon: Associação Passos Mágicos]')

st.markdown(
    """
    <p style='text-indent: 30px'>
    Visando oferecer uma análise detalhada e interativa dos principais indicadores do projeto, apresentamos os dashboards gerados, incluindo gráficos como **Ponto de Virada com Variação Percentual**, **Categorização INDE**, **Evolução do INDE ao Longo dos Anos**, entre outros. Cada gráfico está organizado em sua própria aba, possibilitando a exploração dinâmica dos dados, com a interação direta nos gráficos para obter insights personalizados e visualizar tendências e resultados educacionais de maneira mais envolvente.\n
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([2, 2, 12])  

    with col2:  
        st.image(
            "assets/img/logo_passosmagicos.jpeg", width=512, 
            caption="Logo da Associação Passos Mágicos"
        )
