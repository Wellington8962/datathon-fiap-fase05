import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from tabs.tab import TabInterface


class DistribuicaoPedraTab(TabInterface):
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

            # Filtrar as colunas necessárias e remover valores nulos
            data_filtered = df_clean[['INSTITUICAO_ENSINO_ALUNO_2020', 'INSTITUICAO_ENSINO_ALUNO_2021', 'PEDRA_2020', 'PEDRA_2021']].dropna()

            # Remover entradas com valores '#NULO!' nas colunas de PEDRA_2020 e PEDRA_2021
            data_filtered_final = data_filtered[~data_filtered['PEDRA_2021'].str.contains('#NULO!', na=False)]

            # Contar a quantidade de ocorrências de cada combinação de Instituição e Pedra por ano
            instituicao_pedra_2020_final = data_filtered_final.groupby(['INSTITUICAO_ENSINO_ALUNO_2020', 'PEDRA_2020']).size().unstack(fill_value=0)
            instituicao_pedra_2021_final = data_filtered_final.groupby(['INSTITUICAO_ENSINO_ALUNO_2021', 'PEDRA_2021']).size().unstack(fill_value=0)

            # Filtros interativos
            instituicoes_disponiveis_2020 = list(instituicao_pedra_2020_final.index)
            instituicoes_selecionadas_2020 = st.multiselect('Selecione as Instituições de 2020:', options=instituicoes_disponiveis_2020, default=instituicoes_disponiveis_2020, key='distribuicao_pedra_2020')

            instituicoes_disponiveis_2021 = list(instituicao_pedra_2021_final.index)
            instituicoes_selecionadas_2021 = st.multiselect('Selecione as Instituições de 2021:', options=instituicoes_disponiveis_2021, default=instituicoes_disponiveis_2021, key='distribuicao_pedra_2021')

            tipo_grafico = st.radio("Escolha o tipo de gráfico:", ("Barras", "Linhas"), key='tipo_grafico_distribuicao_pedra')

            # Filtrar os dados com base nas instituições selecionadas
            data_2020_filtrado = instituicao_pedra_2020_final.loc[instituicoes_selecionadas_2020]
            data_2021_filtrado = instituicao_pedra_2021_final.loc[instituicoes_selecionadas_2021]

            # Gerar funcionalidade que mostra os detalhes da visualização escolhida pelo usuário
            instituicoes_2020_str = ', '.join(instituicoes_selecionadas_2020)
            instituicoes_2021_str = ', '.join(instituicoes_selecionadas_2021)
            tipo_grafico_str = f"Tipo de gráfico: {tipo_grafico}."

            with st.expander("Detalhes da Visualização"):
                st.write(f"✅ **Instituições Selecionadas para 2020:** {instituicoes_2020_str}.")
                st.write(f"✅ **Instituições Selecionadas para 2021:** {instituicoes_2021_str}.")
                st.write(f"📊 **{tipo_grafico_str}**")

            # Plotar gráficos com Plotly
            fig_2020 = self.plot_graph(data_2020_filtrado, tipo_grafico, 'Distribuição de Pedra por Instituição em 2020', tick_interval=20)
            fig_2021 = self.plot_graph(data_2021_filtrado, tipo_grafico, 'Distribuição de Pedra por Instituição em 2021', tick_interval=10)

            # Exibir os dois gráficos
            st.plotly_chart(fig_2020)
            st.plotly_chart(fig_2021)

            st.markdown("<br>", unsafe_allow_html=True)

            # Tabela Comparativa
            st.subheader(':blue[Tabela Comparativa de PEDRA por Instituição]', divider='orange')
            tabela_dados_2020 = data_2020_filtrado.reset_index().rename(columns={'INSTITUICAO_ENSINO_ALUNO_2020': 'Instituição'})
            tabela_dados_2021 = data_2021_filtrado.reset_index().rename(columns={'INSTITUICAO_ENSINO_ALUNO_2021': 'Instituição'})

            st.markdown("<h3 style='font-size:22px;'>📅 2020:</h3>", unsafe_allow_html=True)
            st.write(tabela_dados_2020.set_index('Instituição'))

            st.markdown("<h3 style='font-size:22px;'>📆 2021:</h3>", unsafe_allow_html=True)
            st.write(tabela_dados_2021.set_index('Instituição'))

            st.markdown("<br>", unsafe_allow_html=True)

            # Cálculo das métricas de 2020
            total_ametista_2020 = data_2020_filtrado['Ametista'].sum()
            total_quartzo_2020 = data_2020_filtrado['Quartzo'].sum()
            total_topazio_2020 = data_2020_filtrado['Topázio'].sum()
            total_agata_2020 = data_2020_filtrado['Ágata'].sum()

            # Cálculo das métricas de 2021
            total_ametista_2021 = data_2021_filtrado['Ametista'].sum()
            total_quartzo_2021 = data_2021_filtrado['Quartzo'].sum()
            total_topazio_2021 = data_2021_filtrado['Topázio'].sum()
            total_agata_2021 = data_2021_filtrado['Ágata'].sum()

            # Cálculo das porcentagens de 2020
            total_alunos_2020 = data_2020_filtrado.sum().sum()
            pct_ametista_2020 = (total_ametista_2020 / total_alunos_2020) * 100
            pct_quartzo_2020 = (total_quartzo_2020 / total_alunos_2020) * 100
            pct_topazio_2020 = (total_topazio_2020 / total_alunos_2020) * 100
            pct_agata_2020 = (total_agata_2020 / total_alunos_2020) * 100

            # Cálculo das porcentagens de 2021
            total_alunos_2021 = data_2021_filtrado.sum().sum()
            pct_ametista_2021 = (total_ametista_2021 / total_alunos_2021) * 100
            pct_quartzo_2021 = (total_quartzo_2021 / total_alunos_2021) * 100
            pct_topazio_2021 = (total_topazio_2021 / total_alunos_2021) * 100
            pct_agata_2021 = (total_agata_2021 / total_alunos_2021) * 100

            # Exibir as métricas com barras de progresso horizontais
            st.subheader(':blue[Porcentagem de PEDRA por Instituição com Barras de Progresso]', divider='orange')

            col1, col2 = st.columns(2)

            # Para 2020
            with col1:
                st.markdown("<h3 style='font-size:17px;'>🔵 Ametista 2020:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{pct_ametista_2020:.2f}%")
                st.progress(pct_ametista_2020 / 100)

                st.markdown("<h3 style='font-size:17px;'>🟠 Quartzo 2020:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{pct_quartzo_2020:.2f}%")
                st.progress(pct_quartzo_2020 / 100)

            with col2:
                st.markdown("<h3 style='font-size:17px;'>🟢 Topázio 2020:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{pct_topazio_2020:.2f}%")
                st.progress(pct_topazio_2020 / 100)

                st.markdown("<h3 style='font-size:17px;'>🔴 Ágata 2020:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{pct_agata_2020:.2f}%")
                st.progress(pct_agata_2020 / 100)

            st.markdown("<br>", unsafe_allow_html=True)

            # Para 2021
            col3, col4 = st.columns(2)

            with col3:
                st.markdown("<h3 style='font-size:17px;'>🔵 Ametista 2021:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{pct_ametista_2021:.2f}%")
                st.progress(pct_ametista_2021 / 100)

                st.markdown("<h3 style='font-size:17px;'>🟠 Quartzo 2021:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{pct_quartzo_2021:.2f}%")
                st.progress(pct_quartzo_2021 / 100)

            with col4:
                st.markdown("<h3 style='font-size:17px;'>🟢 Topázio 2021:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{pct_topazio_2021:.2f}%")
                st.progress(pct_topazio_2021 / 100)

                st.markdown("<h3 style='font-size:17px;'>🔴 Ágata 2021:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{pct_agata_2021:.2f}%")
                st.progress(pct_agata_2021 / 100)

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados
            csv_data_2020 = tabela_dados_2020.to_csv(index=False).encode('utf-8')
            csv_data_2021 = tabela_dados_2021.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download dos Dados Filtrados de 2020",
                data=csv_data_2020,
                file_name="distribuicao_pedra_2020_dados_filtrados.csv",
                mime="text/csv"
            )
            st.download_button(
                label="Download dos Dados Filtrados de 2021",
                data=csv_data_2021,
                file_name="distribuicao_pedra_2021_dados_filtrados.csv",
                mime="text/csv"
            )

            # Botão para download do gráfico 
            self.download_graph_image(fig_2020, "distribuicao_pedra_2020_grafico.png")
            self.download_graph_image(fig_2021, "distribuicao_pedra_2021_grafico.png")

    def plot_graph(self, data, tipo_grafico, titulo, tick_interval):
        # Criar a figura interativa com Plotly
        fig = go.Figure()

        cores = {
            'Ametista': 'blue',
            'Quartzo': 'orange',
            'Topázio': 'green',
            'Ágata': 'red'
        }

        # Adicionar gráfico para cada categoria de pedra
        for coluna in data.columns:
            if tipo_grafico == "Barras":
                fig.add_trace(go.Bar(
                    y=data.index, x=data[coluna], name=coluna, orientation='h', marker_color=cores.get(coluna, 'gray')
                ))
            elif tipo_grafico == "Linhas":
                fig.add_trace(go.Scatter(
                    y=data.index, x=data[coluna], mode='lines+markers', name=coluna, line=dict(color=cores.get(coluna, 'gray'))
                ))

        # Layout do gráfico
        fig.update_layout(
            title={
                'text': titulo,
                'y': 0.94,
                'x': 0.46,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Número de Alunos',
            yaxis_title='Instituição de Ensino',
            barmode='stack' if tipo_grafico == "Barras" else None,
            plot_bgcolor='white',
            height=600,
            width=780,
            xaxis=dict(
                tickmode='linear',
                dtick=tick_interval
            ),
            yaxis=dict(
                title='Instituição de Ensino',
                automargin=True
            ),
            legend=dict(
                x=0.47,
                y=1.07,
                orientation='h'
            )
        )

        return fig

    def download_graph_image(self, fig, filename):
        # Função para permitir download da imagem do gráfico em PNG
        img_bytes = fig.to_image(format="png")
        st.download_button(
            label=f"Download do Gráfico ({filename.split('_')[2]})",
            data=img_bytes,
            file_name=filename,
            mime="image/png"
        )
