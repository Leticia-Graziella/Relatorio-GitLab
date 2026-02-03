import requests
import datetime as dt
import utils.config as config 


def default_gitlab_request(url: str, method: str = 'GET', headers: dict = None, params: dict = None):
        private_token = config.access_token
        if headers:
            headers['PRIVATE-TOKEN'] = private_token
        else:
            headers = {'PRIVATE-TOKEN': private_token}
        response = requests.request(method, url, headers=headers, params=params)
        if response.status_code == 200:
            return response
        else:
            print(f"Erro ao fazer requisição: {response.status_code} - {response.text}")
            response.raise_for_status()

def get_gitlab_pagination(uri: str, total_pages=-1 ):
    result = []
    current_page = 0
    while uri:
        response = default_gitlab_request(uri)
        result.extend(response.json())
        next_link = response.links.get('next', {}).get('url')
        if next_link and (total_pages == -1 or current_page < total_pages):
            uri = next_link
            current_page += 1
        else:
            uri = None
    return result

def dia_semana(ano, mes,dia):
    data = dt.date(ano,mes,dia)
    dias_semana = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
    dia = dias_semana[data.weekday()]
    return dia

def convercao_hora(segundos):
    if not segundos or segundos == 0:
        return 0.0
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    return f"{horas}.{minutos}"