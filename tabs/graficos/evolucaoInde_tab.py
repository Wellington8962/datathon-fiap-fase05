import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from tabs.tab import TabInterface


class EvolucaoIndeTab(TabInterface):
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

            # Filtrar dados para alunos com e sem ponto de virada
            with_pv = impact_data[(impact_data['PONTO_VIRADA_2020'] == 'Sim') |
                                  (impact_data['PONTO_VIRADA_2021'] == 'Sim') |
                                  (impact_data['PONTO_VIRADA_2022'] == 'Sim')]

            without_pv = impact_data[(impact_data['PONTO_VIRADA_2020'] == 'Não') &
                                     (impact_data['PONTO_VIRADA_2021'] == 'Não') &
                                     (impact_data['PONTO_VIRADA_2022'] == 'Não')]

            # Converter INDE para numérico
            with_pv['INDE_2020'] = pd.to_numeric(with_pv['INDE_2020'], errors='coerce')
            with_pv['INDE_2021'] = pd.to_numeric(with_pv['INDE_2021'], errors='coerce')
            with_pv['INDE_2022'] = pd.to_numeric(with_pv['INDE_2022'], errors='coerce')

            without_pv['INDE_2020'] = pd.to_numeric(without_pv['INDE_2020'], errors='coerce')
            without_pv['INDE_2021'] = pd.to_numeric(without_pv['INDE_2021'], errors='coerce')
            without_pv['INDE_2022'] = pd.to_numeric(without_pv['INDE_2022'], errors='coerce')

            # Calcular as médias do INDE ao longo dos anos para ambos os grupos
            mean_with_pv = with_pv[['INDE_2020', 'INDE_2021', 'INDE_2022']].mean()
            mean_without_pv = without_pv[['INDE_2020', 'INDE_2021', 'INDE_2022']].mean()

            # Filtros interativos
            anos_disponiveis = ['2020', '2021', '2022']
            anos_selecionados = st.multiselect('Selecione os anos:', options=anos_disponiveis, default=anos_disponiveis, key='anos_evolucao_inde')

            tipo_grafico = st.radio("Escolha o tipo de gráfico:", ("Barras", "Linhas"), key='tipo_grafico_evolucao_inde')

            # Aplicar filtro de anos selecionados
            anos_indices = [i for i, ano in enumerate(anos_disponiveis) if ano in anos_selecionados]

            # Aplicar o filtro de anos selecionados para cada grupo
            anos = ['2020', '2021', '2022']
            mean_with_pv_filtrado = [mean_with_pv[i] for i in anos_indices]
            mean_without_pv_filtrado = [mean_without_pv[i] for i in anos_indices]
            anos_filtrados = [anos[i] for i in anos_indices]

            # Cálculo das variações percentuais
            var_with_pv = [0 if i == 0 else (mean_with_pv_filtrado[i] - mean_with_pv_filtrado[i - 1]) / mean_with_pv_filtrado[i - 1] * 100 for i in range(len(mean_with_pv_filtrado))]
            var_without_pv = [0 if i == 0 else (mean_without_pv_filtrado[i] - mean_without_pv_filtrado[i - 1]) / mean_without_pv_filtrado[i - 1] * 100 for i in range(len(mean_without_pv_filtrado))]

            # Gerar funcionalidade que mostra os detalhes da visualização escolhida pelo usuário
            anos_str = ', '.join(anos_selecionados)
            tipo_grafico_str = f"Tipo de gráfico: {tipo_grafico}."

            with st.expander("Detalhes da Visualização"):
                st.write(f"✅ **Anos Selecionados:** {anos_str}.")
                st.write(f"📊 **{tipo_grafico_str}**")

            # Chamar a função que plota o gráfico
            fig = self.plot_graph(anos_filtrados, mean_with_pv_filtrado, mean_without_pv_filtrado, var_with_pv, var_without_pv, tipo_grafico)
            st.plotly_chart(fig)

            st.subheader(':blue[Tabela de Evolução do INDE por Ano]', divider='orange')

            # Exibir tabela com os dados filtrados
            tabela_dados = pd.DataFrame({
                'Ano': anos_filtrados,
                'INDE Médio Com Ponto de Virada': mean_with_pv_filtrado,
                'INDE Médio Sem Ponto de Virada': mean_without_pv_filtrado,
                'Variação Com Ponto de Virada (%)': var_with_pv,
                'Variação Sem Ponto de Virada (%)': var_without_pv
            })
            st.write(tabela_dados.set_index("Ano"))

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(":blue[Métricas de Evolução do INDE]", divider='orange')

            # Exibir métricas com mini gráficos de progresso
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h3 style='font-size:17px;'>📈 INDE Médio Com Ponto de Virada:</h3>", unsafe_allow_html=True)  
                st.metric(label="", value=f"{sum(mean_with_pv_filtrado):.2f}", delta=f"{var_with_pv[-1]:.2f}%")
                st.line_chart(mean_with_pv_filtrado, use_container_width=True)  # Gráfico de progresso para INDE com ponto de virada
            
            with col2:
                st.markdown("<h3 style='font-size:17px;'>📉 INDE Médio Sem Ponto de Virada:</h3>", unsafe_allow_html=True)  
                st.metric(label="", value=f"{sum(mean_without_pv_filtrado):.2f}", delta=f"{var_without_pv[-1]:.2f}%")
                st.line_chart(mean_without_pv_filtrado, use_container_width=True)  # Gráfico de progresso para INDE sem ponto de virada

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados
            csv_data = tabela_dados.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Download dos Dados Filtrados",
                data=csv_data,
                file_name="evolucao_inde_dados_filtrados.csv",
                mime="text/csv"
            )

            # Adicionar botão para download do gráfico como imagem
            self.download_graph_image(fig)

    def plot_graph(self, anos, mean_with_pv, mean_without_pv, var_with_pv, var_without_pv, tipo_grafico):
        # Criar a figura interativa com Plotly
        fig = go.Figure()

        # Adicionar o gráfico com e sem ponto de virada
        if tipo_grafico == "Barras":
            fig.add_trace(go.Bar(x=anos, y=mean_with_pv, name='Com Ponto de Virada', marker_color='blue'))
            fig.add_trace(go.Bar(x=anos, y=mean_without_pv, name='Sem Ponto de Virada', marker_color='green'))
        else:
            fig.add_trace(go.Scatter(x=anos, y=mean_with_pv, mode='lines+markers', name='Com Ponto de Virada', line=dict(color='blue', width=2), marker=dict(size=8)))
            fig.add_trace(go.Scatter(x=anos, y=mean_without_pv, mode='lines+markers', name='Sem Ponto de Virada', line=dict(color='green', width=2), marker=dict(size=8)))

        # Layout do gráfico
        fig.update_layout(
            title={
                'text': 'Evolução do INDE ao Longo dos Anos',
                'y': 0.93,
                'x': 0.45,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Ano',
            yaxis_title='INDE Médio',
            plot_bgcolor='white',
            height=600,
            width=750,
            xaxis=dict(
                tickmode='linear',
                tick0=2020,
                dtick=1
            ),
            legend=dict(
                x=0.56,
                y=1.085,
                orientation='h'
            )
        )

        # Adicionar grid e linhas de estilo
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

        return fig

    def download_graph_image(self, fig):
        # Função para permitir download da imagem do gráfico em PNG
        img_bytes = fig.to_image(format="png")
        st.download_button(
            label="Download do Gráfico",
            data=img_bytes,
            file_name="grafico_evolucao_inde.png",
            mime="image/png"
        )
