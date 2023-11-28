# datajud-monitor
Monitor de processo judicial utilizando API pública do Datajud

Analisando o conteúdo da requisição json para gerar um relatório de andamento processual com o jinja2 em 28/11/2023

resultado: as variáveis foram definidas como:

    numero_processo = dados['hits']['hits'][1]["_source"]["numeroProcesso"]
    tribunal = dados['hits']['hits'][1]["_source"]["tribunal"]
    movimentos = dados['hits']['hits'][1]["_source"]["movimentos"]

## Variáveis do .env

As variáveis incluem diretórios e números de processos. 
Todo 🔜 após os testes, será necessário atualizar os números de processos a partir de uma base de dados

## Exportar as configurações do jinja para as variáveis do.env

A documentação do jinja está disponível em: https://jinja.palletsprojects.com/en/3.1.x/api/#basics

## Relatório em html

Para gerar o relatório em html, é necessário instalar o jinja2 e o beautifulsoup4.

```bash
pip install jinja2 beautifulsoup4
```

O relatório em html, é necessário passar o diretório de saída como parâmetro. Por enquanto isso está sendo feito diretamente no código.  Estudar uma forma de fazer isso dinamicamente a partir do 

```bash
python3 monitor.py /home/user/monitor/output.html

## O script endpoints.py

Recupera os endpoints para a API pública do Datajud.  A ideia é que o usuário possa passar o número de processos e o tribunal para gerar os relatórios

Uma outra forma de fazer isso seria passar o número de processos e o tribunal para o script e gerar o relatório dinamicamente.  Ou seja, o usuário não precisa passar o número de processos.

Ou ainda, pegar o banco de dados de processos cadastrados e fazer a busca pelos endpoins diretamente a partir destes dados.



