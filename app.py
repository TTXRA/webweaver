from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from WebWeaver import webweaver
import logging
import uuid

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/webweaver'
mongo = PyMongo(app)

logging.basicConfig(filename='webweaver.log', level=logging.DEBUG)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        repository = request.form['repository']
        query_type = request.form['query_type']
        query_year = request.form['year']
        search_terms = request.form['search_terms']

        logging.debug(f"Repository: {repository}")
        logging.debug(f"Query Type: {query_type}")
        logging.debug(f"Year: {query_year}")
        logging.debug(f"Search Terms: {search_terms}")

        # Generate a random UUID
        query_id = str(uuid.uuid4())

        webweaver(repository, search_terms, query_type, query_year, query_id)

        repository_collections = {
            "1": "wos",
            "2": "els",
            "3": "bdtd",
        }

        search_terms = search_terms.replace(' ', '+')

        if query_year != "":
            if repository in repository_collections:
                collection_name = f'{search_terms}_{query_year}_{repository_collections[repository]}_{query_id}'
                data_collection = mongo.db[collection_name]
                data = list(data_collection.find())
            else:
                collection_wos = f'{search_terms}_{query_year}_wos_{query_id}'
                collection_els = f'{search_terms}_{query_year}_els_{query_id}'
                collection_bdtd = f'{search_terms}_{query_year}_bdtd_{query_id}'

                data_wos = list(mongo.db[collection_wos].find())
                data_els = list(mongo.db[collection_els].find())
                data_bdtd = list(mongo.db[collection_bdtd].find())

                # Concatenate the data from all three collections into a single list
                data = data_wos + data_els + data_bdtd
        else:
            if repository in repository_collections:
                collection_name = f'{search_terms}_{repository_collections[repository]}_{query_id}'
                data_collection = mongo.db[collection_name]
                data = list(data_collection.find())
            else:
                collection_wos = f'{search_terms}_wos_{query_id}'
                collection_els = f'{search_terms}_els_{query_id}'
                collection_bdtd = f'{search_terms}_bdtd_{query_id}'

                data_wos = list(mongo.db[collection_wos].find())
                data_els = list(mongo.db[collection_els].find())
                data_bdtd = list(mongo.db[collection_bdtd].find())

                # Concatenate the data from all three collections into a single list
                data = data_wos + data_els + data_bdtd

        data_length = len(data)
        logging.debug(f"Data count: {data_length}")

        return render_template('data.html', data=data, data_length=data_length)


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
