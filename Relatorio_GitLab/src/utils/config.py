# CONFIGURANDO GITLAB
# Os valores vêm de variáveis de ambiente para que o token nunca fique no código.
# Exemplo (PowerShell):
#   $env:GITLAB_URL = "https://gitlab.seudominio.com"
#   $env:GITLAB_TOKEN = "seu_token"
#   $env:GITLAB_PROJECT_ID = "123"
import os

gitlab_url = os.environ.get("GITLAB_URL", "https://gitlab.com")
access_token = os.environ.get("GITLAB_TOKEN")
id_projeto = os.environ.get("GITLAB_PROJECT_ID")

if not access_token or not id_projeto:
    raise RuntimeError("Defina as variáveis de ambiente GITLAB_TOKEN e GITLAB_PROJECT_ID antes de rodar o app.")
