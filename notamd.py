import datetime
import os
from rel import ler_arquivo_json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquiv .env
load_dotenv()

# Obter o valor da variável de ambiante OBSIDIAN_DIRECTORY
OBSIDIAN_DIRECTORY = os.getenv("OBSIDIAN_DIRECTORY")


def formatar_data_hora(data_hora):
    data_hora_objeto = datetime.datetime.strptime(data_hora, "%Y-%m-%dT%H:%M:%S.000Z")
    return data_hora_objeto.strftime("%d/%m/%Y %H:%M:%S")


def ordenar_movimentos_por_data(movimentos):
    return sorted(movimentos, key=lambda x: x["dataHora"], reverse=True)

def imprimir_tres_movimentos_recentes(movimentos):
    movimentos_recentes = []
    for movimento in movimentos[:3]:
        nome = movimento["nome"]
        data_hora_legivel = formatar_data_hora(movimento["dataHora"])
        movimento["data_hora_legivel"] = data_hora_legivel  # Adiciona a chave "data_hora_legivel" ao dicionário
        movimentos_recentes.append({"nome": nome, "data_hora_legivel": data_hora_legivel})
        print(" - ", data_hora_legivel, " - ", nome)
    return movimentos_recentes

def incluir_andamentos(nota_obsidian, movimentos):
    nota_obsidian += "\n## Todos os Andamentos\n"
    print("Todos os andamentos:")
    for movimento in movimentos:
        nome = movimento["nome"]
        data_hora_original = movimento["dataHora"]
        data_hora = datetime.datetime.strptime(data_hora_original, "%Y-%m-%dT%H:%M:%S.000Z")
        data_hora_legivel = data_hora.strftime("%d/%m/%Y %H:%M:%S") 
        nota_obsidian += f"- [[{data_hora_legivel} - {nome}]]\n"
        print(" - ", data_hora_legivel, " - ", nome)
    return nota_obsidian


def salvar_nota_obsidian(nota, numero_processo):
    nome_arquivo = f"mov-{numero_processo}.md"
    nome_arquivo_completo = os.path.join(OBSIDIAN_DIRECTORY, nome_arquivo)

    #Verificar se o arquivo já existe
    if os.path.exists(nome_arquivo_completo):
        os.remove(nome_arquivo_completo) #apagar o arquivo existente

    with open(nome_arquivo_completo, "w") as file:
        file.write(nota)

def main():
    dados = ler_arquivo_json("response.json")
    
    numero_processo = dados['hits']['hits'][1]["_source"]["numeroProcesso"]
    tribunal = dados['hits']['hits'][1]["_source"]["tribunal"]
    movimentos = dados['hits']['hits'][1]["_source"]["movimentos"]

    movimentos_ordenados = ordenar_movimentos_por_data(movimentos)

    movimentos_recentes = imprimir_tres_movimentos_recentes(movimentos_ordenados)


    nota_obsidian = f"# Relatório do Processo\n\nNúmero do Processo: {numero_processo}\nTribunal: {tribunal}\n\n## Movimentos Recentes\n"

    for movimento in movimentos_recentes:
        nome = movimento["nome"]
        data_hora_legivel = movimento["data_hora_legivel"]
        nota_obsidian += f"- {data_hora_legivel} - {nome}\n"

    nota_obsidian = incluir_andamentos(nota_obsidian, movimentos_ordenados)

    salvar_nota_obsidian(nota_obsidian, numero_processo)



if __name__ == "__main__":
    main()
