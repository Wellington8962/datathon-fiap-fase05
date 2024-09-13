import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from tabs.tab import TabInterface


class CategorizacaoIndeTab(TabInterface):
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

            # Lista de colunas não relevantes para nosso estudo
            colunas_para_remover = [
                'INSTITUICAO_ENSINO_ALUNO_2020', 'IDADE_ALUNO_2020', 'ANOS_PM_2020', 'FASE_TURMA_2020', 'INDE_CONCEITO_2020',
                'PEDRA_2020', 'DESTAQUE_IEG_2020', 'DESTAQUE_IDA_2020', 'DESTAQUE_IPV_2020', 'FASE_2021', 'TURMA_2021',
                'INSTITUICAO_ENSINO_ALUNO_2021', 'SINALIZADOR_INGRESSANTE_2021', 'PEDRA_2021', 'REC_EQUIPE_1_2021',
                'REC_EQUIPE_2_2021', 'REC_EQUIPE_3_2021', 'REC_EQUIPE_4_2021', 'NIVEL_IDEAL_2021', 'DEFASAGEM_2021',
                'FASE_2022', 'TURMA_2022', 'ANO_INGRESSO_2022', 'BOLSISTA_2022', 'PEDRA_2022', 'DESTAQUE_IEG_2022',
                'DESTAQUE_IDA_2022', 'DESTAQUE_IPV_2022', 'NOTA_PORT_2022', 'NOTA_MAT_2022', 'NOTA_ING_2022', 'QTD_AVAL_2022',
                'REC_AVA_1_2022', 'REC_AVA_2_2022', 'REC_AVA_3_2022', 'REC_AVA_4_2022', 'INDICADO_BOLSA_2022', 'NIVEL_IDEAL_2022'
            ]

            # Criando um DataFrame com as novas colunas
            df_cleaned = df_clean.drop(columns=colunas_para_remover)

            # Convertendo as colunas dos indicadores anuais para formato numérico
            df_cleaned['INDE_2020'] = pd.to_numeric(df_cleaned['INDE_2020'], errors='coerce')
            df_cleaned['INDE_2021'] = pd.to_numeric(df_cleaned['INDE_2021'], errors='coerce')
            df_cleaned['INDE_2022'] = pd.to_numeric(df_cleaned['INDE_2022'], errors='coerce')

            # Filtros interativos com chave única
            anos_disponiveis = ['2020', '2021', '2022']
            anos_selecionados = st.multiselect('Selecione os anos:', options=anos_disponiveis, default=anos_disponiveis, key='anos_categorizacao')

            tipo_grafico = st.radio("Escolha o tipo de gráfico:", ("Barras", "Linhas"), key='tipo_grafico_categorizacao')

            # Aplicar filtro de anos selecionados
            anos_indices = [i for i, ano in enumerate(anos_disponiveis) if ano in anos_selecionados]

            # Função para determinar a tendência com base nas notas
            def calcular_tendencia(inde_2020, inde_2021, inde_2022):
                if inde_2021 > inde_2020 and inde_2022 > inde_2021:
                    return 'Aumento'
                elif inde_2021 < inde_2020 and inde_2022 < inde_2021:
                    return 'Queda'
                elif inde_2021 > inde_2020 and inde_2022 < inde_2021:
                    return 'Aumento seguido de queda'
                elif inde_2021 < inde_2020 and inde_2022 > inde_2021:
                    return 'Queda seguida de aumento'
                elif inde_2020 == inde_2021 and inde_2021 > inde_2022:
                    return 'Queda'
                elif inde_2020 == inde_2021 and inde_2021 < inde_2022:
                    return 'Aumento'
                else:
                    return 'Estável'

            # Aplicando a função para criar a nova coluna INDE_TENDENCIA
            df_cleaned['INDE_TENDENCIA'] = df_cleaned.apply(
                lambda row: calcular_tendencia(row['INDE_2020'], row['INDE_2021'], row['INDE_2022']),
                axis=1
            )

            # Função para calcular a variação percentual
            def calcular_variacao(inde_2020, inde_2022):
                if inde_2020 == 0:
                    if inde_2022 == 0:
                        return 0
                    else:
                        return 'Aumento Infinito'
                else:
                    return ((inde_2022 - inde_2020) / abs(inde_2020)) * 100

            # Aplicando a função para criar a nova coluna INDE_VARIACAO
            df_cleaned['INDE_VARIACAO'] = df_cleaned.apply(
                lambda row: calcular_variacao(row['INDE_2020'], row['INDE_2022']),
                axis=1
            )

            # Contar o número de ocorrências de cada categoria em INDE_TENDENCIA
            tendencia_counts = df_cleaned['INDE_TENDENCIA'].value_counts()

            # Criar uma paleta de cores pastéis
            pastel_palette = sns.color_palette("deep", n_colors=len(tendencia_counts))

            # Gerar funcionalidade que mostra os detalhes da visualização escolhida pelo usuário
            anos_str = ', '.join(anos_selecionados)
            tipo_grafico_str = f"Tipo de gráfico: {tipo_grafico}."

            with st.expander("Detalhes da Visualização"):
                st.write(f"✅ **Anos Selecionados:** {anos_str}.")
                st.write(f"📊 **{tipo_grafico_str}**")

            fig = self.plot_graph(tendencia_counts, tipo_grafico, pastel_palette)
            st.plotly_chart(fig)

            st.subheader(':blue[Tabela de Categorização por Ano]', divider='orange')

            # Verificar o comprimento correto para cada coluna
            anos_filtrados = anos_selecionados
            tendencias_filtradas = tendencia_counts.index.tolist()
            contagens_filtradas = tendencia_counts.values.tolist()

            # Garantir que o tamanho de cada lista seja o mesmo antes de criar o DataFrame
            tamanho_minimo = min(len(anos_filtrados), len(tendencias_filtradas), len(contagens_filtradas))
            tabela_dados = pd.DataFrame({
                'Ano': anos_filtrados[:tamanho_minimo],
                'Tendência': tendencias_filtradas[:tamanho_minimo],
                'Contagem': contagens_filtradas[:tamanho_minimo]
            })
            st.write(tabela_dados.set_index("Ano"))

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(":blue[Métricas com o Total de Tendências]:", divider='orange')

            # Exibir métricas com barras de progresso horizontais para Categorização INDE
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h3 style='font-size:17px;'>🔺 Aumento:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=tendencia_counts.get('Aumento', 0))
                st.progress(tendencia_counts.get('Aumento', 0) / sum(tendencia_counts.values))
            
            with col2:
                st.markdown("<h3 style='font-size:17px;'>🔻 Queda:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=tendencia_counts.get('Queda', 0))
                st.progress(tendencia_counts.get('Queda', 0) / sum(tendencia_counts.values))
            
            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados
            csv_data = tabela_dados.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Download dos Dados Filtrados",
                data=csv_data,
                file_name="categorizacao_inde_dados_filtrados.csv",
                mime="text/csv"
            )

            # Adicionar botão para download do gráfico como imagem
            self.download_graph_image(fig)

    def plot_graph(self, tendencia_counts, tipo_grafico, pastel_palette):
        # Criar a figura interativa com Plotly
        fig = go.Figure()

        # Definir as cores personalizadas conforme o gráfico da imagem
        cores_personalizadas = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Azul, Laranja, Verde, Vermelho

        # Tipo de gráfico: barras ou linhas
        if tipo_grafico == "Barras":
            fig.add_trace(go.Bar(
                x=tendencia_counts.index,
                y=tendencia_counts.values,
                marker_color=cores_personalizadas  # Aplicando as cores personalizadas
            ))
        elif tipo_grafico == "Linhas":
            fig.add_trace(go.Scatter(
                x=tendencia_counts.index,
                y=tendencia_counts.values,
                mode='lines+markers'
            ))

        # Layout do gráfico
        fig.update_layout(
            title={
                'text': 'Categorização INDE',
                'y': 0.93,
                'x': 0.45,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Categoria',
            yaxis_title='Contagem',
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
            file_name="grafico_categorizacao_inde.png",
            mime="image/png"
        )
