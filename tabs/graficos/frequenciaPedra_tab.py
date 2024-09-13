import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from tabs.tab import TabInterface


class FrequenciaPedrasTab(TabInterface):
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

            # Filtros interativos
            anos_disponiveis = ['2020', '2021', '2022']
            anos_selecionados = st.multiselect('Selecione os anos:', options=anos_disponiveis, default=anos_disponiveis, key='anos_frequenciapedra')

            tipo_grafico = st.radio("Escolha o tipo de gráfico:", ("Barras", "Linhas"), key='tipo_grafico_frequenciapedra')

            # Realiza a contagem de valores em cada coluna 'PEDRA'
            count_2020 = df_clean['PEDRA_2020'].value_counts()
            count_2021 = df_clean['PEDRA_2021'].value_counts()
            count_2022 = df_clean['PEDRA_2022'].value_counts()

            # Ordenar as contagens pelas categorias específicas: Topázio, Ametista, Ágata e Quartzo
            ordered_categories = ['Topázio', 'Ametista', 'Ágata', 'Quartzo']

            # Reindexar as contagens com base na ordem desejada
            count_2020 = count_2020.reindex(ordered_categories)
            count_2021 = count_2021.reindex(ordered_categories)
            count_2022 = count_2022.reindex(ordered_categories)

            # Aplicar o filtro de anos selecionados
            contagens = {
                '2020': count_2020,
                '2021': count_2021,
                '2022': count_2022
            }

            anos_filtrados = [ano for ano in anos_selecionados]
            contagens_filtradas = [contagens[ano].fillna(0).values for ano in anos_filtrados]

            # Funcionalidade para mostrar os detalhes da visualização escolhida pelo usuário
            anos_str = ', '.join(anos_selecionados)
            tipo_grafico_str = f"Tipo de gráfico: {tipo_grafico}."

            with st.expander("Detalhes da Visualização"):
                st.write(f"📅 **Anos Selecionados:** {anos_str}.")
                st.write(f"📊 **{tipo_grafico_str}**")

            # Gerar gráfico interativo
            fig = self.plot_graph(anos_filtrados, contagens_filtradas, tipo_grafico)
            st.plotly_chart(fig)

            st.subheader(':blue[Tabela de Frequência de Alunos por Pedras]', divider='orange')

            # Exibir tabela com os dados filtrados
            tabela_dados = pd.DataFrame({
                'Ano': anos_filtrados,
                'Topázio': [contagens[ano].get('Topázio', 0) for ano in anos_filtrados],
                'Ametista': [contagens[ano].get('Ametista', 0) for ano in anos_filtrados],
                'Ágata': [contagens[ano].get('Ágata', 0) for ano in anos_filtrados],
                'Quartzo': [contagens[ano].get('Quartzo', 0) for ano in anos_filtrados],
            })
            st.write(tabela_dados.set_index("Ano"))

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(":blue[Métricas Totais por Categoria de Pedra]", divider='orange')

            # Exibir métricas com mini gráficos de progresso 
            total_topazio = sum(tabela_dados['Topázio'])
            total_ametista = sum(tabela_dados['Ametista'])
            total_agata = sum(tabela_dados['Ágata'])
            total_quartzo = sum(tabela_dados['Quartzo'])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("<h3 style='font-size:17px;'>🟢 Total Topázio:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=total_topazio)
                st.line_chart(tabela_dados['Topázio'], use_container_width=True)

                st.markdown("<h3 style='font-size:17px;'>🔵 Total Ametista:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=total_ametista)
                st.line_chart(tabela_dados['Ametista'], use_container_width=True)

            with col2:
                st.markdown("<h3 style='font-size:17px;'>🔴 Total Ágata:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=total_agata)
                st.line_chart(tabela_dados['Ágata'], use_container_width=True)

                st.markdown("<h3 style='font-size:17px;'>🟠 Total Quartzo:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=total_quartzo)
                st.line_chart(tabela_dados['Quartzo'], use_container_width=True)

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados
            csv_data = tabela_dados.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Download dos Dados Filtrados",
                data=csv_data,
                file_name="frequencia_pedra_dados_filtrados.csv",
                mime="text/csv"
            )

            # Adicionar botão para download do gráfico como imagem
            self.download_graph_image(fig)

    def plot_graph(self, anos, contagens, tipo_grafico):
        # Criar a figura interativa com Plotly
        fig = go.Figure()

        categorias = ['Topázio', 'Ametista', 'Ágata', 'Quartzo']
        cores = ['green', 'blue', 'red', 'orange']

        # Tipo de gráfico: barras ou linhas
        if tipo_grafico == "Barras":
            for i, categoria in enumerate(categorias):
                fig.add_trace(go.Bar(x=anos, y=[contagem[i] for contagem in contagens], name=categoria, marker_color=cores[i]))
        elif tipo_grafico == "Linhas":
            for i, categoria in enumerate(categorias):
                fig.add_trace(go.Scatter(x=anos, y=[contagem[i] for contagem in contagens], mode='lines+markers', name=categoria, marker=dict(color=cores[i], size=10)))

        # Layout do gráfico
        fig.update_layout(
            title={
                'text': 'Distribuição de Alunos por Categoria de Pedra (2020-2022)',
                'y': 0.93,  
                'x': 0.45,  
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Ano',
            xaxis=dict(type='category'),  
            yaxis=dict(
                title='Frequência',
                showgrid=True,  
                gridwidth=0.5,  
                gridcolor='LightGrey' 
            ),
            barmode='group',
            legend=dict(
                x=0.5,  
                y=1.05,  
                orientation='h',  
            ),
            plot_bgcolor='white',  
            height=600,
            width=800
        )

        return fig

    def download_graph_image(self, fig):
        # Função para permitir download da imagem do gráfico em PNG
        img_bytes = fig.to_image(format="png")
        st.download_button(
            label="Download do Gráfico",
            data=img_bytes,
            file_name="grafico_frequencia_pedra.png",
            mime="image/png"
        )
