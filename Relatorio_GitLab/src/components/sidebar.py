import streamlit as st
import pandas as pd
from buscaDados import buscar_issues_filtradas

dado_cb = buscar_issues_filtradas()

# Converter datas e criar colunas auxiliares
dado_cb["DATA ENTREGA"] = pd.to_datetime(dado_cb["DATA ENTREGA"])
dado_cb["Mes"] = dado_cb["DATA ENTREGA"].dt.to_period("M").astype(str)
dado_cb["Dia"] = dado_cb["DATA ENTREGA"].dt.date
dado_cb["RESPOSÁVEL"] = dado_cb["RESPOSÁVEL"].astype(str)
dado_cb["CLASSIFICAÇÃO"] = dado_cb["CLASSIFICAÇÃO"].astype(str)
 
# CRIANDO FILTROS 


def sidebar():
    st.sidebar.header("Filtros")
    
    #FILTRO DE RESPONSAVEL 
    integrador = ["Todos"] + sorted(dado_cb["RESPOSÁVEL"].unique())
    integrador_sel = st.sidebar.selectbox("RESPOSÁVEL", integrador)

    integrador_filt = dado_cb
    if integrador_sel != "Todos":
        integrador_filt = dado_cb[dado_cb["RESPOSÁVEL"] == integrador_sel]

    #FILTRO DE SQUAD
    squad = ["Todos"] + sorted(dado_cb["SQUAD"].unique())
    squad_sel = st.sidebar.selectbox("SQUAD", squad)

    if squad_sel != "Todos":
        integrador_filt = dado_cb[dado_cb["SQUAD"] == squad_sel]
        

    #Filtro de fila 
    fila = ["Todos"] + sorted(dado_cb["ESTÁGIO DO CHAMADO"].unique())
    fila_sel = st.sidebar.selectbox("FILA", fila)
    if fila_sel != "Todos":
        integrador_filt = dado_cb[dado_cb["ESTÁGIO DO CHAMADO"] == fila_sel]

 

    
    return integrador_sel, squad_sel, fila_sel, integrador_filt,