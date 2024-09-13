import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from tabs.tab import TabInterface


class PontoViradaTab(TabInterface):
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
            df_cleaned['IAA_2020'] = pd.to_numeric(df_cleaned['IAA_2020'], errors='coerce')
            df_cleaned['IEG_2020'] = pd.to_numeric(df_cleaned['IEG_2020'], errors='coerce')
            df_cleaned['IPS_2020'] = pd.to_numeric(df_cleaned['IPS_2020'], errors='coerce')
            df_cleaned['IDA_2020'] = pd.to_numeric(df_cleaned['IDA_2020'], errors='coerce')
            df_cleaned['IPP_2020'] = pd.to_numeric(df_cleaned['IPP_2020'], errors='coerce')
            df_cleaned['IPV_2020'] = pd.to_numeric(df_cleaned['IPV_2020'], errors='coerce')
            df_cleaned['IAN_2020'] = pd.to_numeric(df_cleaned['IAN_2020'], errors='coerce')
            df_cleaned['INDE_2021'] = pd.to_numeric(df_cleaned['INDE_2021'], errors='coerce')
            df_cleaned['IAA_2021'] = pd.to_numeric(df_cleaned['IAA_2021'], errors='coerce')
            df_cleaned['IEG_2021'] = pd.to_numeric(df_cleaned['IEG_2021'], errors='coerce')
            df_cleaned['IPS_2021'] = pd.to_numeric(df_cleaned['IPS_2021'], errors='coerce')
            df_cleaned['IDA_2021'] = pd.to_numeric(df_cleaned['IDA_2021'], errors='coerce')
            df_cleaned['IPP_2021'] = pd.to_numeric(df_cleaned['IPP_2021'], errors='coerce')
            df_cleaned['IPV_2021'] = pd.to_numeric(df_cleaned['IPV_2021'], errors='coerce')
            df_cleaned['IAN_2021'] = pd.to_numeric(df_cleaned['IAN_2021'], errors='coerce')
            df_cleaned['INDE_2022'] = pd.to_numeric(df_cleaned['INDE_2022'], errors='coerce')
            df_cleaned['CG_2022'] = pd.to_numeric(df_cleaned['CG_2022'], errors='coerce')
            df_cleaned['CF_2022'] = pd.to_numeric(df_cleaned['CF_2022'], errors='coerce')
            df_cleaned['CT_2022'] = pd.to_numeric(df_cleaned['CT_2022'], errors='coerce')
            df_cleaned['IAA_2022'] = pd.to_numeric(df_cleaned['IAA_2022'], errors='coerce')
            df_cleaned['IEG_2022'] = pd.to_numeric(df_cleaned['IEG_2022'], errors='coerce')
            df_cleaned['IPS_2022'] = pd.to_numeric(df_cleaned['IPS_2022'], errors='coerce')
            df_cleaned['IDA_2022'] = pd.to_numeric(df_cleaned['IDA_2022'], errors='coerce')
            df_cleaned['IPP_2022'] = pd.to_numeric(df_cleaned['IPP_2022'], errors='coerce')
            df_cleaned['IPV_2022'] = pd.to_numeric(df_cleaned['IPV_2022'], errors='coerce')
            df_cleaned['IAN_2022'] = pd.to_numeric(df_cleaned['IAN_2022'], errors='coerce')

            # Filtros interativos
            anos_disponiveis = ['2020', '2021', '2022']
            anos_selecionados = st.multiselect('Selecione os anos:', options=anos_disponiveis, default=anos_disponiveis, key='anos_pontovirada')

            tipo_grafico = st.radio("Escolha o tipo de gráfico:", ("Barras", "Linhas"), key='tipo_grafico_pontovirada')

            # Contar o número de "Sim" e "Não" para cada ano
            contagem_2020 = df_cleaned['PONTO_VIRADA_2020'].value_counts()
            contagem_2021 = df_cleaned['PONTO_VIRADA_2021'].value_counts()
            contagem_2022 = df_cleaned['PONTO_VIRADA_2022'].value_counts()

            anos = ['2020', '2021', '2022']
            sim = [contagem_2020.get('Sim', 0), contagem_2021.get('Sim', 0), contagem_2022.get('Sim', 0)]
            nao = [contagem_2020.get('Não', 0), contagem_2021.get('Não', 0), contagem_2022.get('Não', 0)]

            # Aplicar o filtro de anos selecionados
            anos_indices = [i for i, ano in enumerate(anos) if ano in anos_selecionados]
            anos_filtrados = [anos[i] for i in anos_indices]
            sim_filtrado = [sim[i] for i in anos_indices]
            nao_filtrado = [nao[i] for i in anos_indices]

            # Cálculo das variações percentuais
            var_sim = [0 if i == 0 else (sim_filtrado[i] - sim_filtrado[i - 1]) / sim_filtrado[i - 1] * 100 if sim_filtrado[i - 1] != 0 else 0 for i in range(len(sim_filtrado))]
            var_nao = [0 if i == 0 else (nao_filtrado[i] - nao_filtrado[i - 1]) / nao_filtrado[i - 1] * 100 if nao_filtrado[i - 1] != 0 else 0 for i in range(len(nao_filtrado))]

            # Gerar funcionalidade que mostra os detalhes da visualização escolhida pelo usuário
            anos_str = ', '.join(anos_selecionados)
            tipo_grafico_str = f"Tipo de gráfico: {tipo_grafico}."

            with st.expander("Detalhes da Visualização"):
                st.write(f"✅ **Anos Selecionados:** {anos_str}.")
                st.write(f"📊 **{tipo_grafico_str}**")

            fig = self.plot_graph(anos_filtrados, sim_filtrado, nao_filtrado, var_sim, var_nao, tipo_grafico)
            st.plotly_chart(fig)

            st.subheader(':blue[Tabela de Ponto de Virada por Ano]', divider='orange')

            # Exibir tabela com os dados filtrados
            tabela_dados = pd.DataFrame({
                'Ano': anos_filtrados,
                'Sim': sim_filtrado,
                'Não': nao_filtrado,
                'Variação Sim (%)': var_sim,
                'Variação Não (%)': var_nao
            })
            st.write(tabela_dados.set_index("Ano"))

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(":blue[Métricas com o Total de 'Sim' e 'Não']", divider='orange')

            # Exibir métricas com mini gráficos de progresso 
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("<h3 style='font-size:17px;'>✅ Total de 'Sim':</h3>", unsafe_allow_html=True)  
                st.metric(label="", value=sum(sim_filtrado), delta=f"{var_sim[-1]:.2f}%")
                st.line_chart(sim_filtrado, use_container_width=True)  

            with col2:
                st.markdown("<h3 style='font-size:17px;'>❌ Total de 'Não':</h3>", unsafe_allow_html=True) 
                st.metric(label="", value=sum(nao_filtrado), delta=f"{var_nao[-1]:.2f}%")
                st.line_chart(nao_filtrado, use_container_width=True)  

            st.subheader(':blue[Exportação de Dados e Gráficos]', divider='orange')

            # Botão para download dos dados filtrados
            csv_data = tabela_dados.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Download dos Dados Filtrados",
                data=csv_data,
                file_name="ponto_de_virada_dados_filtrados.csv",
                mime="text/csv"
            )

            # Adicionar botão para download do gráfico como imagem
            self.download_graph_image(fig)

    def plot_graph(self, anos, sim, nao, var_sim, var_nao, tipo_grafico):
        # Criar a figura interativa com Plotly
        fig = go.Figure()

        # Tipo de gráfico: barras ou linhas
        if tipo_grafico == "Barras":
            fig.add_trace(go.Bar(x=anos, y=sim, name='Sim', marker_color='blue'))
            fig.add_trace(go.Bar(x=anos, y=nao, name='Não', marker_color='#A5D6A7'))
        elif tipo_grafico == "Linhas":
            fig.add_trace(go.Scatter(x=anos, y=sim, mode='lines+markers', name='Sim', marker=dict(color='blue', size=10)))
            fig.add_trace(go.Scatter(x=anos, y=nao, mode='lines+markers', name='Não', marker=dict(color='#A5D6A7', size=10)))

        # Adicionar as linhas de variação percentual
        fig.add_trace(go.Scatter(
            x=anos,
            y=var_sim,
            mode='lines+markers',
            name='Variação Sim (%)',
            marker=dict(color='green', size=10),
            line=dict(color='green', width=2),
            yaxis='y2'  
        ))

        fig.add_trace(go.Scatter(
            x=anos,
            y=var_nao,
            mode='lines+markers',
            name='Variação Não (%)',
            marker=dict(color='red', size=10),
            line=dict(color='red', width=2),
            yaxis='y2'  
        ))

        # Layout do gráfico
        fig.update_layout(
            title={
                'text': 'Ponto de Virada com Variação Percentual',
                'y': 0.93,  
                'x': 0.45,  
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Ano',
            xaxis=dict(type='category'),  
            yaxis=dict(
                title='Contagem',
                showgrid=True,  
                gridwidth=0.5,  
                gridcolor='LightGrey' 
            ),
            yaxis2=dict(
                title='Variação Percentual (%)',
                overlaying='y',  
                side='right',
                showgrid=False  
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
            file_name="grafico_ponto_de_virada.png",
            mime="image/png"
        )
