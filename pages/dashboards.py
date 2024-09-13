import streamlit as st
from tabs.graficos.pontoVirada_tab import PontoViradaTab
from tabs.graficos.categorizacaoInde_tab import CategorizacaoIndeTab
from tabs.graficos.evolucaoInde_tab import EvolucaoIndeTab
from tabs.graficos.distribuicaoPedra_tab import DistribuicaoPedraTab
from tabs.graficos.comparacaoPedra_tab import ComparacaoPedraTab
from tabs.graficos.correlacaoIndicadores_tab import CorrelacaoIndicadoresTab
from tabs.graficos.diferencaInde_tab import DiferencaIndeTab
from tabs.graficos.notasDisciplina_tab import NotasDisciplinaTab
from tabs.graficos.frequenciaPedra_tab import FrequenciaPedrasTab
from util.layout import output_layout

st.set_page_config(page_title="Dashboards | Datathon | FIAP", layout='wide')
output_layout()

with st.container():
    st.header(':blue[Análises Gráficas Interativas: Descubra os Dados Através de Dashboards]',divider="orange")

    st.markdown(
    """
    <p style='text-indent: 30px'>
    Nesta seção do aplicativo, você encontrará todos os gráficos e análises geradas no nosso projeto Datathon. Explore as diferentes visualizações interativas e filtre os dados para obter insights personalizados.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <small>Para **:blue[navegar entre as abas]**, posicione o mouse em cima das abas e segure a tecla **:blue[[SHIFT]]** e utilize o botão central de scroll do mouse 🖱</small>
    """,
    unsafe_allow_html=True
)


tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    tabs=[
        ":one: Pontos de Virada",
        ":two: Categorização INDE",
        ":three: Evolução INDE",
        ":four: INDE vs Pedra",
        ":five: Distribuição de Pedras por Instituição",
        ":six: Correlação Indicadores",
        ":seven: Diferenças INDE",
        ":eight: Notas por Disciplina 2022",
        ":nine: Distribuição de Alunos por Pedra"
    ]
)
PontoViradaTab(tab0)
CategorizacaoIndeTab(tab1)
EvolucaoIndeTab(tab2)
ComparacaoPedraTab(tab3)
DistribuicaoPedraTab(tab4)
CorrelacaoIndicadoresTab(tab5)
DiferencaIndeTab(tab6)
NotasDisciplinaTab(tab7)
FrequenciaPedrasTab(tab8)
    