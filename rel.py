from jinja2 import Template
import json

# Lê o arquivo JSON
with open("response.json", "r") as file:
    dados = json.load(file)

# todo criar variáveis com todas as informações contidas no json para compor o relatório 
movimentos = dados['hits']['hits'][1]['_source']['movimentos']

# todo retirar o modelo jinja para outro arquivo
# Template HTML
template_html = """
jinja2
<table>
    <thead>
        <tr>
            <th>Código</th>
            <th>Nome</th>
            <th>Data e Hora</th>
            <th>Complementos Tabelados</th>
        </tr>
    </thead>
    <tbody>
        {% for item in dados %}
        <tr>
            <td>{{ item.codigo }}</td>
            <td>{{ item.nome }}</td>
            <td>{{ item.dataHora }}</td>
            <td>
                {% if item.complementosTabelados %}
                    <ul>
                        {% for complemento in item.complementosTabelados %}
                            <li>
                                Código: {{ complemento.codigo }},
                                Valor: {{ complemento.valor }},
                                Nome: {{ complemento.nome }},
                                Descrição: {{ complemento.descricao }}
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    Nenhum complemento tabelado encontrado.
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<h2>Movimentos do Processo:</h2>
<ul>
    {% for movimento in movimentos %}
        <li>{{ movimento }}</li>
    {% endfor %}
</ul>
"""

# Cria o template Jinja2
template = Template(template_html)

# Renderiza o template com os dados e movimentos
relatorio_html = template.render(dados=dados, movimentos=movimentos)

# Salva o relatório em um arquivo HTML
with open("relatorio.html", "w") as file:
    file.write(relatorio_html)
