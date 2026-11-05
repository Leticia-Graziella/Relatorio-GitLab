# Relatório de Chamados (relatorio-chamados)

Aplicação em Streamlit para consultar e gerar relatórios de issues do GitLab (chamados), filtrando por labels, squad, owner, datas e tempo de trabalho. O app busca issues via API do GitLab, processa labels e campos relevantes e exibe um relatório interativo.

## Principais arquivos

- `src/relatorio.py` - Entrada da aplicação Streamlit (UI e interação).
- `src/buscaDados.py` - Funções para buscar e filtrar issues na API do GitLab.
- `utils/config.py` - Configurações do projeto (token, URL do GitLab, id do projeto).
- `utils/func.py` - Funções utilitárias (conversão de horas, dia da semana etc.).
- `data/sample_issues.csv` - Exemplo de dados para testes locais.

## Requisitos

- Python 3.10+ (recomendado)
- `pip` instalado

Instale dependências a partir do `requirements.txt`:

```powershell
pip install -r requirements.txt
```

## Configuração

O app lê as configurações de variáveis de ambiente (veja `src/utils/config.py`). Nunca coloque o token direto no código.

- `GITLAB_TOKEN` - Token do GitLab com permissão de leitura (`read_api`).
- `GITLAB_URL` - URL base do GitLab (padrão: `https://gitlab.com`).
- `GITLAB_PROJECT_ID` - ID do projeto GitLab a consultar.

Exemplo (PowerShell):

```powershell
$env:GITLAB_URL = "https://gitlab.seudominio.com"
$env:GITLAB_TOKEN = "SEU_TOKEN_AQUI"
$env:GITLAB_PROJECT_ID = "123456"
```

## Como executar (desenvolvimento)

A aplicação é um app Streamlit. Rode o servidor com:

```powershell
streamlit run src/relatorio.py
```

Isto abrirá a interface web localmente (por padrão `http://localhost:8501`).

## Uso

- A interface permite selecionar filtros (projeto, estado do issue, responsável, data de atualização etc.).
- O módulo `src/buscaDados.py` faz a chamada à API e aplica filtros de labels, calcula prazos e classifica os chamados em `PROBLEMA`, `RISCO` ou `Ok`.
- Campos importantes exibidos no relatório: título do chamado, responsável(s), owner, data de entrega, dias restantes, squad, projeto, estágio do chamado, tipo, classificação, tempo estimado e tempo gasto.

## Troubleshooting

- Erro 401/403: verifique se `access_token` tem permissões corretas.
- Resposta inesperada da API: `src/buscaDados.py` já tenta tratar resposta não-lista e imprime conteúdo para debugging.
