from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import datetime
import webbrowser
from dotenv import load_dotenv

def ler_arquivo_json(nome_arquivo):
    with open(nome_arquivo, "r") as file:
        return json.load(file)

def criar_ambiente_jinja2():
    return Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )

def imprimir_informacoes(numero_processo, tribunal, movimentos):
    print("Número do processo:", numero_processo)
    print("Tribunal:", tribunal)
    print("Movimentos:")
    for movimento in movimentos:
        nome = movimento["nome"]
        data_hora_original = movimento["dataHora"]
        data_hora = datetime.datetime.strptime(data_hora_original, "%Y-%m-%dT%H:%M:%S.%fZ")
        data_hora_legivel = data_hora.strftime("%d/%m/%Y %H:%M:%S")
        print(" - ", data_hora_legivel, " - ", nome)
        movimento["dataHora"] = data_hora

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

def main():
    dados = ler_arquivo_json("response.json")
    env = criar_ambiente_jinja2()
    template = env.get_template("template.html")
    
    numero_processo = dados['hits']['hits'][1]["_source"]["numeroProcesso"]
    tribunal = dados['hits']['hits'][1]["_source"]["tribunal"]
    movimentos = dados['hits']['hits'][1]["_source"]["movimentos"]

    imprimir_informacoes(numero_processo, tribunal, movimentos)

    movimentos_ordenados = ordenar_movimentos_por_data(movimentos)

    movimentos_recentes = imprimir_tres_movimentos_recentes(movimentos_ordenados)

    relatorio_html = renderizar_template(template, numero_processo, tribunal, movimentos, movimentos_recentes)

    salvar_relatorio_html(relatorio_html, "relatorio.html")

    # abrir relatório no navegador
    webbrowser.open("relatorio.html")

if __name__ == "__main__":
    main()
