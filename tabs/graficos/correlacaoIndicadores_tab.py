import streamlit as st
import pandas as pd
import plotly.express as px
from tabs.tab import TabInterface

class CorrelacaoIndicadoresTab(TabInterface):
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

            # Selecionar as colunas de interesse para correlação
            correlation_columns = [
                'INDE_2020', 'INDE_2021', 'INDE_2022',
                'IAA_2020', 'IAA_2021', 'IAA_2022',
                'IDA_2020', 'IDA_2021', 'IDA_2022',
                'IEG_2020', 'IEG_2021', 'IEG_2022',
                'IPS_2020', 'IPS_2021', 'IPS_2022',
                'IPP_2020', 'IPP_2021', 'IPP_2022'
            ]

            # Criar uma nova tabela com as colunas de interesse
            correlation_data = df_clean[correlation_columns].apply(pd.to_numeric, errors='coerce')

            # Calcular a matriz de correlação
            correlation_matrix = correlation_data.corr()

            # Escolher a escala de cores
            color_scale_option = st.selectbox(
                'Escolha a Escala de Cores:',
                options=['RdBu_r','Bluered', 'Viridis', 'Spectral', 'Picnic'],
                index=0
            )

            # Gerar funcionalidade que mostra os detalhes da visualização escolhida pelo usuário
            with st.expander("Detalhes da Visualização"):
                st.write("✅ **Indicadores Selecionados para o Heatmap de Correlação:**")
                st.write(", ".join(correlation_columns))

            # Plotar o heatmap de correlação usando Plotly Express
            fig = self.plot_heatmap(correlation_matrix, color_scale_option)

            # Exibir o gráfico
            st.plotly_chart(fig)

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados (correlação)
            csv_data = correlation_matrix.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Download da Matriz de Correlação",
                data=csv_data,
                file_name="matriz_correlacao_indicadores.csv",
                mime="text/csv"
            )

            # Adicionar botão para download do gráfico
            self.download_graph_image(fig, "heatmap_correlacao_indicadores.png")

    def plot_heatmap(self, correlation_matrix, color_scale):
        # Criar heatmap interativo com Plotly Express
        fig = px.imshow(
            correlation_matrix,
            labels=dict(color="Correlação"),
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            color_continuous_scale=color_scale,  # Usar a escala de cores escolhida
            zmin=-1, zmax=1,  # Definir o intervalo de valores para a correlação (de -1 a 1)
            aspect="auto"
        )

        # Customizar o layout
        fig.update_layout(
            title={
                'text': 'Heatmap de Correlação entre Indicadores (2020 a 2022)',
                'y': 0.955,
                'x': 0.45,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_nticks=36,
            yaxis_nticks=36,
            width=800,
            height=700,
            coloraxis_colorbar=dict(
                title="Correlação",
                tickvals=[-1, -0.5, 0, 0.5, 1],  # Personalizar ticks na barra de cores
                ticktext=["-1 (Negativa)", "-0.5", "0 (Neutra)", "0.5", "1 (Positiva)"]
            )
        )

        return fig

    def download_graph_image(self, fig, filename):
        # Função para permitir download da imagem do gráfico em PNG
        img_bytes = fig.to_image(format="png")
        st.download_button(
            label=f"Download do Gráfico",
            data=img_bytes,
            file_name=filename,
            mime="image/png"
        )
