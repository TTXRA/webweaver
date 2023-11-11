from pymongo import MongoClient


def save(data_list, query, query_date, query_id, total, database):
    # Conecta ao MongoDB.
    client = MongoClient('mongodb://localhost:27017/')

    # Seleciona ou cria um banco de dados.
    db = client['webweaver']

    # Seleciona ou cria uma coleção.
    if query_date != "":
        collection = db[f'{query}_{query_date}_{database}_{query_id}']
    else:
        collection = db[f'{query}_{database}_{query_id}']

    # Insere os dados no MongoDB.
    result = collection.insert_many(data_list)

    if result.acknowledged:
        # Verifica o valor da variável 'database' para identificar o repositório.
        match database:
            case 'els':
                repository = 'Scopus'
            case 'wos':
                repository = 'Web of Science'
            case 'bdtd':
                repository = 'BDTD'

        # Exibe uma mensagem indicando o número de itens inseridos.
        if total == '1':
            print(f"{len(data_list)} de {total} item disponível em {repository} foi inserido no MongoDB.")
        else:
            print(f"{len(data_list)} de {total} itens disponíveis em {repository} foram inseridos no MongoDB.")
    else:
        print(f"Não foi possível inserir os dados no MongoDB.")