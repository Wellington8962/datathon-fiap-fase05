import streamlit as st
from st_pages import show_pages, Page

def output_layout():
    show_pages(
        [
            Page("./main.py", "Datathon: Fase 5", ":computer:", use_relative_hash=True),
            Page(
                "./pages/dashboards.py",
                "Dashboards",
                ":chart_with_upwards_trend:",
                use_relative_hash=True,
            ),

              Page(
                "./pages/links_documentos.py",
                "Documentos do Projeto",
                ":memo:",
                use_relative_hash=True,
            ),
        ]
    )
    
    with st.sidebar:
        st.subheader("Integrantes do Projeto:")
        st.text("André Luiz Pedroso (RM353107)") 
        st.text("David Robert de Oliveira (RM352754)")
        st.text("Lucas Rana Rosa Fernandes (RM353105)") 
        st.text("Raphael Gottstein Alves dos Santos (RM353054)")
        st.text("Wellington Porto Brito (RM352977)")
        st.subheader("Turma")
        st.text("3DTAT")   



        
  
