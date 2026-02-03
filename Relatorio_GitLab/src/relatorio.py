import streamlit as st
import plotly_express as px
from buscaDados import buscar_issues_filtradas, colorir
from components.sidebar import sidebar as sb


st.write("### Relatório de Chamados em Risco")

#Aumentando a largura da tabela
st.set_page_config(layout="wide")

# Buscando dados
dado_cb = buscar_issues_filtradas()
#sb()  # Chama a função sidebar para aplicar os filtros
integrador_sel, squad_sel, fila_sel, integrador_filt = sb()
 

col1,col2,col3,col4, col5, = st.columns(5)

#Gráfico de barras - Chamados em risco
qts_risco = integrador_filt["CLASSIFICAÇÃO"].value_counts().reset_index()
qts_risco.columns = ["CLASSIFICAÇÃO", "Quantidade"]
fig_risco = px.bar(qts_risco, x="CLASSIFICAÇÃO", y="Quantidade", title="Chamados em risco")
fig_risco.update_layout(xaxis_tickangle=-45, barmode="group")
col1.plotly_chart(fig_risco)

#Gráfico de pizza - Chamados abertos
qts_abertos = integrador_filt["CLASSIFICAÇÃO"].value_counts().reset_index()
qts_abertos.columns = ["CLASSIFICAÇÃO", "TOTAL"]
fig_chamados_abertos = px.pie(qts_abertos, values="TOTAL", names="CLASSIFICAÇÃO", title="Chamados abertos")
col3.plotly_chart(fig_chamados_abertos, use_container_width=True)

#Tabela de chamados abertos 
total_geral = qts_abertos["TOTAL"].sum()# Soma total dos valores
qts_abertos.loc[len(qts_abertos)] = ["Total Geral", total_geral]# Adiciona linha com Total Geral
col5.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
col5.dataframe(qts_abertos)

#Visão em tabela dos chamados de risco
chamados = buscar_issues_filtradas() #Chamando demandas de sustentação
    # Aplica filtro por integrador
if integrador_sel != "Todos":
    chamados = integrador_filt[integrador_filt["RESPOSÁVEL"] == integrador_sel]
# Aplica filtro por squad
if squad_sel != "Todos":
    chamados = chamados[chamados["SQUAD"] == squad_sel]
# Aplica filtro por Fila
if fila_sel != "Todos":
    chamados = chamados[chamados["ESTÁGIO DO CHAMADO"] == fila_sel]

st.dataframe(chamados.style.applymap(colorir, subset=["DATA ENTREGA"]).format(precision=0), hide_index=False)
