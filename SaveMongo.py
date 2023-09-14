from pymongo import MongoClient


def save(data_list, query, query_date, total, database):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')

    # Select or create a database
    db = client['webweaver']

    # Select or create a collection
    collection = db[f'{query}_{database}_{query_date}']

    # Insert the data into MongoDB
    result = collection.insert_many(data_list)

    # Print the inserted document IDs
    print("Inserted IDs:", result.inserted_ids)

    # Check the value of the 'database' variable to determine the repository
    if database == 'els':
        repository = 'Scopus'
    elif database == 'wos':
        repository = 'Web of Science'
    else:
        repository = 'DBTD'

    # Print a message indicating the number of items inserted
    print(f"Inserted {len(data_list)} from {total} {repository} items into MongoDB.")