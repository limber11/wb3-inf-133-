# Definir la consulta GraphQL con parametros
query_lista = """
{
        estudiante_por_Id(id: 2{
            nombre
        }
    }
"""

# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query})
print(response.text)