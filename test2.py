import os
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import json
import webbrowser

def ordenar_movimentos_por_data(movimentos):
    return sorted(movimentos, key=lambda x: x["dataHora"], reverse=True)

def imprimir_tres_movimentos_recentes(movimentos):
    print("Três movimentos mais recentes:")
    movimentos_recentes = []
    for movimento in movimentos[:3]:
        nome = movimento["nome"]
        data_hora_legivel = movimento["dataHora"].strftime("%d/%m/%Y %H:%M:%S")
        movimentos_recentes.append({"nome": nome, "data_hora_legivel": data_hora_legivel})
        print(" - ", data_hora_legivel, " - ", nome)
    return movimentos_recentes

def renderizar_template(template, numero_processo, tribunal, movimentos, movimentos_recentes):
    return template.render(numero_processo=numero_processo, tribunal=tribunal, movimentos=movimentos, movimentos_recentes=movimentos_recentes)

def salvar_relatorio_html(relatorio_html, nome_arquivo):
    with open(nome_arquivo, "w") as file:
        file.write(relatorio_html)

def gerar_nota_obsidian(numero_processo, movimentos_recentes):
    nome_arquivo = f"andamentos{numero_processo}.md"
    diretorio = os.getenv("OBSIDIAN_DIRECTORY")
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    with open(caminho_arquivo, "w") as file:
        file.write(f"Número do processo: {numero_processo}\n")
        file.write("Três movimentos mais recentes:\n")
        for movimento in movimentos_recentes:
            nome = movimento["nome"]
            data_hora_legivel = movimento["data_hora_legivel"]
            file.write(f"- {data_hora_legivel} - {nome}\n")

def main():
    with open("response copy.json", "r") as file:
        dados = json.load(file)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    load_dotenv()

    numero_processo = dados['hits']['hits'][1]["_source"]["numeroProcesso"]
    tribunal = dados['hits']['hits'][1]["_source"]["tribunal"]
    movimentos = dados['hits']['hits'][1]["_source"]["movimentos"]

    movimentos_recentes = imprimir_tres_movimentos_recentes(movimentos)
    relatorio_html = renderizar_template(template, numero_processo, tribunal, movimentos, movimentos_recentes)
    salvar_relatorio_html(relatorio_html, "relatorio.html")
    #abrir relatório no navegador
    webbrowser.open("relatorio.html")
    gerar_nota_obsidian(numero_processo, movimentos_recentes)
