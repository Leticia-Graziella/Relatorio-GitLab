import requests
import pandas as pd
import datetime as dt
import streamlit as st
import utils.config as config
import utils.func as func
from dateutil import parser

@st.cache_data(ttl=3600)
def buscar_issues_filtradas(projeto=config.id_projeto, state="opened", assignee_id=None, updated_after=None, per_page=2000):  
    headers = {"PRIVATE-TOKEN": config.access_token}
    params = {
        "state": state,
        "per_page": per_page
    }
    if assignee_id:
        params["assignee_id"] = assignee_id
    if updated_after:
        params["updated_after"] = updated_after

    url = f"{config.gitlab_url}/api/v4/projects/{projeto}/issues"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Erro {response.status_code}: {response.text}")
   
    try:
        issues_raw = response.json()
        if not isinstance(issues_raw, list):
          print("Erro: resposta inesperada da API:")
          print(issues_raw)
          return pd.DataFrame()  # retorna vazio
    except Exception as e:
        print("Erro ao decodificar JSON:", e)
        print(response.text)
        return pd.DataFrame()
    
    labels_desejadas = {"New","Triado","Incompleto","Desenvolvimento", "Code Review","Validacao","SLA","Sustentacao","Desenvolvimento Interno","Projetos Estruturantes","Implantação"}
    label_projeto = {"Sustentacao","Projetos Estruturantes","Implantação"}
    labels_complexidade = {"C1","C2","C3"}
    labels_classe = {"Atualizacao SHP","Atualizacao TBLF","Correção Pontual","Correção Script","Dados Incorretos ERP","Enriquecimento","Erro de Integracao","Erro no envio de dados","Estrutura","Extracao de dados","Integracao Reversa","QA","Regras de Negocio","Spick"}
  
    issues_filtradas = []
    for issue in issues_raw:
        todas_labels = issue.get("labels", [])

        #FILTRAGEM DE LABELS
        labels_owner = [
            label for label in todas_labels
            if  label.startswith("Owner") or label.startswith("owner")
        ]
        labels_squad = [
            label for label in todas_labels
            if  label.startswith("Squad") or label == "AirFlow" or label =="Octopus"
        ]
        
        if not labels_squad :
                labels_squad = ["SEM SQUAD"]
        labels_filtradas = [
            label for label in todas_labels
            if label in labels_desejadas or label.startswith("Squad") or label.startswith("Owner")
        ]
        label_projeto = [
            label for label in labels_filtradas
            if label =="Implantação" or label =="Sustentacao" or label.startswith("Projetos")
        ]
        label_estagio_chamado = [
             label for label in labels_filtradas
            if label =="New" or label =="Triado" or label =="Incompleto" or label =="Desenvolvimento" or label =="Code Review" or label =="Validacao" 
        ]
        label_tp_chamado = [
             label for label in labels_filtradas
            if label =="Desenvolvimento Interno" or label =="SLA"  or label =="Projetos Estruturantes"  or label =="Implantação"
        ]

        if issue.get("due_date") :
            due_date = dt.datetime.strptime(issue.get("due_date"), "%Y-%m-%d").date()
        else:
            due_date =  dt.date(2026, 9, 30)

        if due_date <= dt.date.today() :
            
            classificacao = 'PROBLEMA'
        elif due_date == dt.date.today() + dt.timedelta(days=1) or due_date == dt.date.today() + dt.timedelta(days = 2) or (func.dia_semana( dt.date.today().year, dt.date.today().month, dt.date.today().day) == "Quinta" and  due_date == dt.date.today() + dt.timedelta(days = 4))or(func.dia_semana( dt.date.today().year, dt.date.today().month, dt.date.today().day) == "Sexta" and (due_date == dt.date.today() + dt.timedelta(days = 3) or due_date == dt.date.today() + dt.timedelta(days = 4)) ) :
            classificacao = 'RISCO'
        else :
            classificacao = 'Ok'   
        
        dias_faltantes = due_date - dt.date.today() 
        time_stats = issue.get("time_stats", {})
        labels_complex = [
                label for label in todas_labels
                if label in labels_complexidade
            ]
        labels_class = [
                label for label in todas_labels
                if label in labels_classe
            ]

        if label_estagio_chamado :
            issues_filtradas.append({
                "CHAMADO": issue.get("title"),
                "RESPOSÁVEL": ", ".join([a["username"] for a in issue.get("assignees", [])]),
                "OWNER": ", ".join([nome[6:] for nome in labels_owner]),
                "DATA ENTREGA": due_date,
                "DATADE CRIAÇÃO": parser.parse(issue.get("created_at")).date(),
                "DATA DA ULTIMA ATUALIZAÇÃO": parser.parse(issue.get("updated_at")).date(),
                "DIAS FALTANTE":(str(dias_faltantes.days)),
                "SQUAD": ", ".join(labels_squad),
                "PROJETO" : ", ".join(label_projeto),
                "ESTÁGIO DO CHAMADO" : ", ".join(label_estagio_chamado),
                "TIPO DO CHAMADO" : ", ".join(label_tp_chamado),
                "CLASSIFICAÇÃO" : classificacao,
                "TEMPO ESTIMADO": func.convercao_hora(time_stats.get("time_estimate")),
                "TEMPO TOTAL GASTO": func.convercao_hora(time_stats.get("total_time_spent")),
                "COMPLEXIDADE" :  ", ".join(labels_complex),
                "CLASSE DE RESOLUÇÃO" :  ", ".join(labels_class)
                })
    
    df = pd.DataFrame(issues_filtradas)
   
    return df

def colorir(val) :
    if isinstance(val, (pd.Timestamp, dt.datetime, dt.date)):
        if val < dt.date.today() :
            return "color: red"
        elif val == dt.date.today() :
            return "color: purple"
        elif val == dt.date.today() + dt.timedelta(days=1) or val == dt.date.today() + dt.timedelta(days = 2) or (func.dia_semana( dt.date.today().year, dt.date.today().month, dt.date.today().day) == "Quinta" and  val == dt.date.today() + dt.timedelta(days = 4))or(func.dia_semana( dt.date.today().year, dt.date.today().month, dt.date.today().day) == "Sexta" and (val == dt.date.today() + dt.timedelta(days = 3) or val == dt.date.today() + dt.timedelta(days = 4)) )  :
            return "color: yellow"
        else:
            return "color: green"
