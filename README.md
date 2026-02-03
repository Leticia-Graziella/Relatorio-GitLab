# Relatorio-GitLab

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

Edite `utils/config.py` com as credenciais e parâmetros do projeto. O arquivo deve prover pelo menos as variáveis (nomes aproximados usados pelo projeto):

- `access_token` - Token privado do GitLab com permissão para ler issues.
- `gitlab_url` - URL base do GitLab (ex: `https://gitlab.com` ou sua instância interna).
- `id_projeto` - ID do projeto GitLab a consultar.

Exemplo mínimo :

```python
# utils/config.py (exemplo)
access_token = "SEU_TOKEN_AQUI"
gitlab_url = "https://gitlab.com"
id_projeto = 123456
```

Alternativa (recomendada): mantenha o token em variáveis de ambiente e modifique `utils/config.py` para lê-las com `os.environ`.

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
