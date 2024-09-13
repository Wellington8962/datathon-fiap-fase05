import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tabs.tab import TabInterface

class NotasDisciplinaTab(TabInterface):
    def __init__(self, tab):
        self.tab = tab
        self.render()

    def render(self):
        with self.tab:
            # Carregar os dados
            file_path = './dataset/PEDE_PASSOS_DATASET_FIAP.csv'
            df = pd.read_csv(file_path, sep=';')

            # Renomear as colunas
            df = df.rename(columns={
                'NOTA_PORT_2022': 'Portugues',
                'NOTA_MAT_2022': 'Matematica',
                'NOTA_ING_2022': 'Ingles'
            })

            # Preparar os dados
            columns_to_analyze = ['Portugues', 'Matematica', 'Ingles']
            df[columns_to_analyze] = df[columns_to_analyze].apply(pd.to_numeric, errors='coerce')
            df_clean = df.dropna(subset=columns_to_analyze)

            # Filtros interativos
            disciplinas = ['Portugues', 'Matematica', 'Ingles']
            disciplinas_selecionadas = st.multiselect(
                'Selecione as Disciplinas:', options=disciplinas, default=disciplinas, key='disciplinas_notas'
            )

            tipo_grafico = st.radio("Escolha o tipo de gráfico:", ("Boxplot", "Violin Plot", "Histograma"), key='tipo_grafico_notas')

            # Aplicar filtros com base nas disciplinas selecionadas
            df_filtrado = df_clean[disciplinas_selecionadas]

            # Gerar funcionalidade que mostra os detalhes da visualização escolhida pelo usuário
            disciplinas_str = ', '.join(disciplinas_selecionadas)
            tipo_grafico_str = f"Tipo de gráfico: {tipo_grafico}."

            with st.expander("Detalhes da Visualização"):
                st.write(f"📚 **Disciplinas Selecionadas:** {disciplinas_str}.")
                st.write(f"📊 **{tipo_grafico_str}**")

            # Plotar gráfico Boxplot, Violin Plot ou Histograma individual por disciplina
            if tipo_grafico == "Boxplot":
                fig = px.box(df_filtrado.melt(var_name='Disciplinas', value_name='Notas'), x='Disciplinas', y='Notas', points="all", title='Distribuição das Notas por Disciplina (2022)')
            elif tipo_grafico == "Violin Plot":
                fig = px.violin(df_filtrado.melt(var_name='Disciplinas', value_name='Notas'), x='Disciplinas', y='Notas', points="all", title='Distribuição das Notas por Disciplina (2022)')
            elif tipo_grafico == "Histograma":
                # Criar um histograma separado para cada disciplina selecionada
                for disciplina in disciplinas_selecionadas:
                    fig = px.histogram(df_clean, x=disciplina, nbins=20, title=f'Histograma de {disciplina} (2022)', color_discrete_sequence=['lightblue'])
                    fig.update_traces(marker_line=dict(width=0.5, color='black'))
                    fig.update_layout(
                        xaxis=dict(
                            title='Notas'  
                        ),
                        yaxis=dict(
                            title='Frequência',
                            showgrid=True,
                            gridcolor='lightgray',
                        ),
                        title={
                            'text': f'Histograma das Notas de {disciplina} (2022)',
                            'y': 0.91,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        },
                        font=dict(
                            family="Arial, sans-serif",
                            size=14  
                        ),
                        plot_bgcolor='#f7f7f7',  # Background mais claro
                        paper_bgcolor='#f7f7f7',  # Fundo geral da figura
                        hoverlabel=dict(
                            bgcolor="white",
                            font_size=14,
                            font_family="Arial"
                        ),
                        margin=dict(l=50, r=50, t=80, b=50),
                        showlegend=False
                    )
                    # Exibir o histograma para cada disciplina
                    st.plotly_chart(fig)

            # Layout do gráfico
            if tipo_grafico in ["Boxplot", "Violin Plot"]:
                fig.update_layout(
                    xaxis=dict(
                        title='Disciplinas'
                    ),
                    yaxis=dict(
                        title='Notas',
                        showgrid=True,
                        gridcolor='lightgray',
                    ),
                    title={
                        'text': 'Distribuição das Notas por Disciplina (2022)',
                        'y': 0.91,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                    },
                    font=dict(
                        family="Arial, sans-serif",
                        size=14  
                    ),
                    plot_bgcolor='#f7f7f7',  # Background mais claro
                    paper_bgcolor='#f7f7f7',  # Fundo geral da figura
                    hoverlabel=dict(
                        bgcolor="white",
                        font_size=14,
                        font_family="Arial"
                    ),
                    margin=dict(l=50, r=50, t=80, b=50),  # Ajustar margens
                    showlegend=False
                )

                # Exibir o gráfico
                st.plotly_chart(fig)

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(':blue[Resumo Estatístico de Notas por Disciplina]', divider='orange')

            # Exibir resumo estatístico e ajustar os nomes para português
            resumo_estatistico = df_filtrado.describe()

            # Renomear as linhas para português
            resumo_estatistico = resumo_estatistico.rename(index={
                'count': 'Contagem',
                'mean': 'Média',
                'std': 'Desvio Padrão',
                'min': 'Mínimo',
                '25%': '1º Quartil (25%)',
                '50%': 'Mediana (50%)',
                '75%': '3º Quartil (75%)',
                'max': 'Máximo'
            })

            # Adicionar nome à primeira coluna (por exemplo, 'Estatística')
            resumo_estatistico.index.name = 'Estatística'

            # Exibir o resumo ajustado
            st.write(resumo_estatistico)

            st.markdown("<br>", unsafe_allow_html=True)

            # Gráfico "Média das Notas por Disciplina (2022)" 
            st.subheader(':blue[Média das Notas por Disciplina (2022)]', divider='orange')
            
            means = df_clean[columns_to_analyze].mean()

            # Criar o gráfico de barras 
            fig_means = go.Figure(
                data=[go.Bar(
                    x=means.index,
                    y=means.values,
                    text=[f'{value:.2f}' for value in means.values],
                    textposition='auto',
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'], 
                    hoverinfo='text'
                )]
            )

            # Adicionar título e ajustar layout do gráfico
            fig_means.update_layout(
                title={
                'text': 'Média das Notas por Disciplina (2022)',
                'y': 0.91,
                'x': 0.46,
                'xanchor': 'center',
                'yanchor': 'top'
            },
                xaxis_title="Disciplina",
                yaxis_title="Média",
                font=dict(
                    family="Arial, sans-serif",
                    size=14
                ),
                plot_bgcolor='#f7f7f7',
                paper_bgcolor='#f7f7f7',
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=14,
                    font_family="Arial"
                ),
                margin=dict(l=50, r=50, t=70, b=50),  
                showlegend=False,
                bargap=0.3, 
            )

            # Exibir o gráfico de barras no Streamlit
            st.plotly_chart(fig_means)

            st.markdown("<br>", unsafe_allow_html=True)

            # Exibir Métricas Dinâmicas com barras de progresso
            st.subheader(':blue[Visão Geral das Notas (Disciplinas Combinadas)]', divider='orange')

            media = df_filtrado.mean().mean()
            maxima = df_filtrado.max().max()
            minima = df_filtrado.min().min()
            desvio_padrao = df_filtrado.std().std()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("<h3 style='font-size:17px;'>📈 Média das Notas:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{media:.2f}")
                st.progress(media / 10)  # Supondo que a nota máxima seja 10

                st.markdown("<h3 style='font-size:17px;'>📊 Nota Máxima:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{maxima:.2f}")
                st.progress(maxima / 10)

            with col2:
                st.markdown("<h3 style='font-size:17px;'>📉 Nota Mínima:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{minima:.2f}")
                st.progress(minima / 10)

                st.markdown("<h3 style='font-size:17px;'>📉 Desvio Padrão:</h3>", unsafe_allow_html=True)
                st.metric(label="", value=f"{desvio_padrao:.2f}")
                st.progress(desvio_padrao / 10)

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados
            csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download dos Dados Filtrados",
                data=csv_data,
                file_name="notas_dados_filtrados.csv",
                mime="text/csv"
            )

            # Botão para download do gráfico de Boxplot ou Violin Plot
            self.download_graph_image(fig, "grafico_notas.png")

    def download_graph_image(self, fig, filename):
        # Função para permitir download da imagem do gráfico em PNG
        img_bytes = fig.to_image(format="png")
        st.download_button(
            label="Download do Gráfico",
            data=img_bytes,
            file_name=filename,
            mime="image/png"
        )
