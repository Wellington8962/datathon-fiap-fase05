import streamlit as st
from util.layout import output_layout

st.set_page_config(page_title="Documentos do Projeto | Datathon | FIAP", layout='wide')
output_layout()

with st.container():
    st.header(':blue[Documentos do Projeto]', divider="orange")

    # Explicação do conteúdo da página
    st.markdown(
        """
        <p style='text-indent: 30px; font-size:16px; line-height:1.6'>
        Nesta seção, você encontrará os principais documentos do projeto Datathon, que é parte do nosso trabalho de conclusão de curso da Pós-Tech em Data Analytics. 
        Esses arquivos incluem a apresentação e o relatório do projeto, que são essenciais para compreender as etapas do desenvolvimento, 
        as análises realizadas, os insights gerados, e as recomendações feitas para a Passos Mágicos.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Link para o Google Drive com cor azul-escuro e tamanho ajustado
    st.markdown(
        """
        <h4 style="font-size:20px; color:#1f4e79; font-weight:bold;">
        🔗 <a href="https://drive.google.com/drive/folders/1WhohZoVhO2nSbj6JcFK-bmzWRjMDNTRK?usp=sharing" style="color:#1f4e79;">Acesse os Documentos do Projeto</a>
        </h4>
        
        <div style="margin-left: 30px;">
        <p style='font-size:16px;'>
        <strong>Arquivos disponíveis:</strong>
        <ol>
            <li>Código Fonte Streamlit do Projeto (Fiap-Datathon)</li>
            <li>Pasta com os Arquivos em Python (Jupyter Notebooks) e Base de Dados (CSV)</li>
            <li>Vídeo da Apresentação (MP4)</li>
            <li>Apresentação do Projeto (PDF)</li>
            <li>Apresentação do Projeto (.pptx)</li>
            <li>Relatório do Projeto (PDF)</li>
            <li>Relatório do Projeto (.docx)</li>
        </ol>
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
