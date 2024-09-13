import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from tabs.tab import TabInterface


class ComparacaoPedraTab(TabInterface):
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

            # Filtrar os dados para alunos com categorias "Pedra"
            pedra_categories = ['Topázio', 'Ametista', 'Ágata', 'Quartzo']
            comparison_data = df_clean[
                df_clean['PEDRA_2020'].isin(pedra_categories) &
                df_clean['PEDRA_2021'].isin(pedra_categories) &
                df_clean['PEDRA_2022'].isin(pedra_categories)
            ]

            # Converter colunas INDE para tipo numérico
            comparison_data['INDE_2020'] = pd.to_numeric(comparison_data['INDE_2020'], errors='coerce')
            comparison_data['INDE_2021'] = pd.to_numeric(comparison_data['INDE_2021'], errors='coerce')
            comparison_data['INDE_2022'] = pd.to_numeric(comparison_data['INDE_2022'], errors='coerce')

            # Filtros interativos
            pedras_disponiveis = ['Topázio', 'Ametista', 'Ágata', 'Quartzo']
            pedras_selecionadas = st.multiselect('Selecione as categorias de Pedra:', options=pedras_disponiveis, default=pedras_disponiveis)

            tipo_grafico = st.radio("Escolha o tipo de gráfico:", ("Barras", "Linhas"))

            # Filtrar os dados com base nas categorias de pedras selecionadas
            comparison_data_filtrado = comparison_data[comparison_data['PEDRA_2020'].isin(pedras_selecionadas)]

            # Calcular a média do INDE para cada categoria de Pedra em cada ano
            mean_inde_by_pedra = comparison_data_filtrado.groupby('PEDRA_2020')[['INDE_2020', 'INDE_2021', 'INDE_2022']].mean()

             # Calcular a média dos três anos (2020, 2021, 2022) para cada pedra
            mean_inde_by_pedra['INDE_Media_2020_2022'] = mean_inde_by_pedra[['INDE_2020', 'INDE_2021', 'INDE_2022']].mean(axis=1)

            # Aplicar filtro de pedras selecionadas
            pedras_filtradas = list(mean_inde_by_pedra.index)

            # Ordem de exibição das pedras no gráfico
            pedras_filtradas = ['Topázio', 'Ametista', 'Ágata', 'Quartzo']
            mean_inde_by_pedra = mean_inde_by_pedra.reindex(pedras_filtradas)

            # Gerar funcionalidade que mostra os detalhes da visualização escolhida pelo usuário
            pedras_str = ', '.join(pedras_selecionadas)
            tipo_grafico_str = f"Tipo de gráfico: {tipo_grafico}."

            with st.expander("Detalhes da Visualização"):
                st.write(f"✅ **Categorias de Pedra Selecionadas:** {pedras_str}.")
                st.write(f"📊 **{tipo_grafico_str}**")

            # Gerar gráfico com Plotly
            fig = self.plot_graph(pedras_filtradas, mean_inde_by_pedra, tipo_grafico)
            st.plotly_chart(fig)

            st.markdown("<br>", unsafe_allow_html=True)    

            # Exibir Tabela Comparativa
            st.subheader(':blue[Tabela Comparativa do INDE por Categoria de Pedra]', divider='orange')
            tabela_dados = mean_inde_by_pedra.reset_index().rename(columns={'PEDRA_2020': 'PEDRA'})
            tabela_dados = tabela_dados.set_index("PEDRA")
            st.write(tabela_dados)

            st.markdown("<br>", unsafe_allow_html=True)

             # Exibir Métricas com a média dos três anos
            st.subheader(":blue[Métricas de INDE por Categoria de Pedra]", divider='orange')

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1:
                st.markdown("<h3 style='font-size:17px;'>🔵 INDE Médio Topázio:</h3>", unsafe_allow_html=True)  
                st.metric(label="", value=f"{mean_inde_by_pedra.loc['Topázio', 'INDE_Media_2020_2022']:.2f}")
                st.line_chart(mean_inde_by_pedra.loc['Topázio', ['INDE_2020', 'INDE_2021', 'INDE_2022']])

            with col2:
                st.markdown("<h3 style='font-size:17px;'>🟠 INDE Médio Ametista:</h3>", unsafe_allow_html=True)  
                st.metric(label="", value=f"{mean_inde_by_pedra.loc['Ametista', 'INDE_Media_2020_2022']:.2f}")
                st.line_chart(mean_inde_by_pedra.loc['Ametista', ['INDE_2020', 'INDE_2021', 'INDE_2022']])

            with col3:
                st.markdown("<h3 style='font-size:17px;'>🟢 INDE Médio Ágata:</h3>", unsafe_allow_html=True)  
                st.metric(label="", value=f"{mean_inde_by_pedra.loc['Ágata', 'INDE_Media_2020_2022']:.2f}")
                st.line_chart(mean_inde_by_pedra.loc['Ágata', ['INDE_2020', 'INDE_2021', 'INDE_2022']])

            with col4:
                st.markdown("<h3 style='font-size:17px;'>🔴 INDE Médio Quartzo:</h3>", unsafe_allow_html=True)  
                st.metric(label="", value=f"{mean_inde_by_pedra.loc['Quartzo', 'INDE_Media_2020_2022']:.2f}")
                st.line_chart(mean_inde_by_pedra.loc['Quartzo', ['INDE_2020', 'INDE_2021', 'INDE_2022']])

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados
            csv_data = tabela_dados.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download dos Dados Filtrados",
                data=csv_data,
                file_name="comparacao_pedra_dados_filtrados.csv",
                mime="text/csv"
            )

            # Adicionar botão para download do gráfico como imagem
            self.download_graph_image(fig)

    def plot_graph(self, pedras, mean_inde_by_pedra, tipo_grafico):
        # Criar a figura interativa com Plotly
        fig = go.Figure()

        # Adicionar gráfico de barras ou linhas baseado na escolha do usuário
        if tipo_grafico == "Barras":
            fig.add_trace(go.Bar(
                x=pedras, y=mean_inde_by_pedra['INDE_2020'], name='INDE 2020', marker_color='blue'
            ))
            fig.add_trace(go.Bar(
                x=pedras, y=mean_inde_by_pedra['INDE_2021'], name='INDE 2021', marker_color='orange'
            ))
            fig.add_trace(go.Bar(
                x=pedras, y=mean_inde_by_pedra['INDE_2022'], name='INDE 2022', marker_color='green'
            ))
        elif tipo_grafico == "Linhas":
            fig.add_trace(go.Scatter(
                x=pedras, y=mean_inde_by_pedra['INDE_2020'], mode='lines+markers', name='INDE 2020', line=dict(color='blue')
            ))
            fig.add_trace(go.Scatter(
                x=pedras, y=mean_inde_by_pedra['INDE_2021'], mode='lines+markers', name='INDE 2021', line=dict(color='orange')
            ))
            fig.add_trace(go.Scatter(
                x=pedras, y=mean_inde_by_pedra['INDE_2022'], mode='lines+markers', name='INDE 2022', line=dict(color='green')
            ))

        # Layout do gráfico
        fig.update_layout(
            title={
                'text': 'Comparação do INDE por Categoria de Pedra (2020, 2021, 2022)',
                'y': 0.93,
                'x': 0.48,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Categoria de Pedra',
            yaxis_title='INDE Médio',
            barmode='group' if tipo_grafico == "Barras" else None,
            plot_bgcolor='white',
            height=600,
            width=800,
            xaxis=dict(
                tickmode='linear',
                tickangle=-45
            ),
            legend=dict(
                x=0.60,
                y=1.05,
                orientation='h'
            )
        )

        return fig

    def download_graph_image(self, fig):
        # Função para permitir download da imagem do gráfico em PNG
        img_bytes = fig.to_image(format="png")
        st.download_button(
            label="Download do Gráfico",
            data=img_bytes,
            file_name="comparacao_pedra_grafico.png",
            mime="image/png"
        )
