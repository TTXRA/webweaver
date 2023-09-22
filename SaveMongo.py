from pymongo import MongoClient


def save(data_list, query, query_date, query_id, total, database):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')

    # Select or create a database
    db = client['webweaver']

    # Select or create a collection
    if query_date != "":
        collection = db[f'{query}_{query_date}_{database}_{query_id}']
    else:
        collection = db[f'{query}_{database}_{query_id}']

    # Insert the data into MongoDB
    result = collection.insert_many(data_list)

    # Check the value of the 'database' variable to determine the repository
    if database == 'els':
        repository = 'Scopus'
    elif database == 'wos':
        repository = 'Web of Science'
    else:
        repository = 'DBTD'

    # Print a message indicating the number of items inserted
    print(f"Inserted {len(data_list)} from {total} {repository} items into MongoDB.")