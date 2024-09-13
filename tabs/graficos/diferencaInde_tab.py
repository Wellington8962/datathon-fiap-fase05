import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from tabs.tab import TabInterface


class DiferencaIndeTab(TabInterface):
    def __init__(self, tab):
        self.tab = tab
        self.render()

    def render(self):
        with self.tab:
            # Carregar os dados
            file_path = './dataset/PEDE_PASSOS_DATASET_FIAP.csv'
            df = pd.read_csv(file_path, delimiter=';')

            # Preparar os dados
            df_clean = df.dropna()

            # Filtrar as colunas relevantes para análise
            columns_of_interest = [
                'NOME', 'PONTO_VIRADA_2020', 'PONTO_VIRADA_2021', 'PONTO_VIRADA_2022',
                'INDE_2020', 'INDE_2021', 'INDE_2022'
            ]

            impact_data = df_clean[columns_of_interest]

            # Verificar se existem alunos com pontos de virada nos diferentes anos
            pontos_virada = impact_data[
                (impact_data['PONTO_VIRADA_2020'] == 'Sim') |
                (impact_data['PONTO_VIRADA_2021'] == 'Sim') |
                (impact_data['PONTO_VIRADA_2022'] == 'Sim')
            ]

            # Converter colunas INDE para numérico, ignorando erros para evitar problemas com valores não numéricos
            pontos_virada['INDE_2020'] = pd.to_numeric(pontos_virada['INDE_2020'], errors='coerce')
            pontos_virada['INDE_2021'] = pd.to_numeric(pontos_virada['INDE_2021'], errors='coerce')
            pontos_virada['INDE_2022'] = pd.to_numeric(pontos_virada['INDE_2022'], errors='coerce')

            # Remover valores nulos após a conversão
            pontos_virada.dropna(subset=['INDE_2020', 'INDE_2021', 'INDE_2022'], inplace=True)

            # Calcular as diferenças de INDE ano a ano
            pontos_virada['DIF_INDE_2020_2021'] = pontos_virada['INDE_2021'] - pontos_virada['INDE_2020']
            pontos_virada['DIF_INDE_2021_2022'] = pontos_virada['INDE_2022'] - pontos_virada['INDE_2021']

            # Filtros interativos para os Pontos de Virada
            pontos_virada_selecionados = st.multiselect(
                'Selecione os Pontos de Virada:',
                options=['Sim', 'Não'],
                default=['Sim'],
                key='pontos_virada_selecionados'
            )

            # Aplicar filtros com base nas seleções do usuário
            dados_filtrados = pontos_virada[
                (pontos_virada['PONTO_VIRADA_2020'].isin(pontos_virada_selecionados)) |
                (pontos_virada['PONTO_VIRADA_2021'].isin(pontos_virada_selecionados)) |
                (pontos_virada['PONTO_VIRADA_2022'].isin(pontos_virada_selecionados))
            ]

            # Detalhes da visualização
            with st.expander("Detalhes da Visualização"):
                st.write(f"📊 **Pontos de Virada Selecionados:** {', '.join(pontos_virada_selecionados)}")
                st.write(f"📈 **Tipo de Gráfico:** Histograma")

            # Gráfico de diferença no INDE de 2020 para 2021
            fig_2020_2021 = go.Figure(data=[go.Histogram(
                x=dados_filtrados['DIF_INDE_2020_2021'].dropna(),
                nbinsx=20,  
                marker_color='blue',
                marker_line=dict(width=0.5, color='black'), 
            )])

            fig_2020_2021.update_layout(
                xaxis_title="Diferença no INDE",
                yaxis=dict(
                    title='Número de Alunos',
                    showgrid=True,  
                    gridcolor='lightgray'  
                ),
                title={
                    'text': 'Diferença no INDE de 2020 para 2021',
                    'y': 0.85,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                },
                font=dict(
                    family="Arial, sans-serif",
                    size=14  
                )
            )

            # Gráfico de diferença no INDE de 2021 para 2022
            fig_2021_2022 = go.Figure(data=[go.Histogram(
                x=dados_filtrados['DIF_INDE_2021_2022'].dropna(),
                nbinsx=20,  
                marker_color='green',
                marker_line=dict(width=0.5, color='black'), 
            )])

            fig_2021_2022.update_layout(
                xaxis_title="Diferença no INDE",
                yaxis=dict(
                    title='Número de Alunos',
                    showgrid=True,  
                    gridcolor='lightgray'  
                ),
                title={
                    'text': 'Diferença no INDE de 2021 para 2022',
                    'y': 0.85,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                },
                font=dict(
                    family="Arial, sans-serif", 
                    size=14  
                )
            )

            # Exibir os gráficos
            st.plotly_chart(fig_2020_2021)
            st.plotly_chart(fig_2021_2022)

            st.markdown("<br>", unsafe_allow_html=True)

            # Remover a Tabela Comparativa de Diferenças no INDE e adicionar novas métricas
            st.subheader(':blue[Métricas Dinâmicas de Diferença INDE]', divider='orange')

            # Adicionar ícones, cores e explicação
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("<h3 style='font-size:17px; color:#2D9CDB;'>📈 Diferença Positiva INDE 2020-2021:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=dados_filtrados[dados_filtrados['DIF_INDE_2020_2021'] > 0].shape[0])
                st.markdown("<h3 style='font-size:17px; color:#EB5757;'>📉 Diferença Negativa INDE 2020-2021:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=dados_filtrados[dados_filtrados['DIF_INDE_2020_2021'] < 0].shape[0])

            with col2:
                st.markdown("<h3 style='font-size:17px; color:#2D9CDB;'>📈 Diferença Positiva INDE 2021-2022:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=dados_filtrados[dados_filtrados['DIF_INDE_2021_2022'] > 0].shape[0])
                st.markdown("<h3 style='font-size:17px; color:#EB5757;'>📉 Diferença Negativa INDE 2021-2022:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=dados_filtrados[dados_filtrados['DIF_INDE_2021_2022'] < 0].shape[0])

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                "<div style='font-size:17px; display:inline-block;'>📝 <strong>Observação:</strong></div>"
                "<span style='font-size:17px;'> Os valores exibidos representam o <strong>número total de alunos</strong> que apresentaram diferenças positivas ou negativas no INDE (Índice de Desenvolvimento Educacional) entre os anos 2020-2021 e 2021-2022. Uma diferença positiva significa que o aluno teve uma melhora no índice de um ano para o outro, enquanto uma diferença negativa indica uma queda no desempenho.</span>",
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados
            csv_data = dados_filtrados.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download dos Dados Filtrados",
                data=csv_data,
                file_name="diferenca_inde_dados_filtrados.csv",
                mime="text/csv"
            )

            # Botão para download do gráfico
            self.download_graph_image(fig_2020_2021, "diferenca_inde_2020_2021_grafico.png")
            self.download_graph_image(fig_2021_2022, "diferenca_inde_2021_2022_grafico.png")

    def download_graph_image(self, fig, filename):
        # Função para permitir download da imagem do gráfico em PNG
        img_bytes = fig.to_image(format="png")
        st.download_button(
            label=f"Download do Gráfico ({filename.split('_')[2]})",
            data=img_bytes,
            file_name=filename,
            mime="image/png"
        )
