from bson import ObjectId
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from WebWeaver import webweaver
import logging
import uuid
import random
import json
import os
import shutil

app = Flask(__name__)
app.config['TEMP_DATA_DIR'] = 'temp_data'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/webweaver'
mongo = PyMongo(app)

logging.basicConfig(filename='webweaver.log', level=logging.DEBUG)


def process_data(repository, search_terms, query_type, query_year, query_id):
    total = webweaver(repository, search_terms, query_type, query_year, query_id)

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

    return data, total


def json_serializable(data):
    for item in data:
        for key, value in item.items():
            if isinstance(value, ObjectId):
                item[key] = str(value)
    return data


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        repository = request.form['repository']
        query_type = request.form['query_type']
        query_year = request.form['year']
        search_terms = request.form['search_terms']

        # Generate a random UUID
        query_id = str(uuid.uuid4())

        result = process_data(repository, search_terms, query_type, query_year, query_id)
        data, total = result

        if len(data):
            # Generate a unique token for this data
            token = str(uuid.uuid4())

            # Store the data on the server temporarily
            data_dir = os.path.join(app.config['TEMP_DATA_DIR'], token)
            os.makedirs(data_dir)
            with open(os.path.join(data_dir, 'data.json'), 'w') as file:
                json.dump(json_serializable(data), file)
            random.shuffle(data)

            return render_template('data.html', data=data, data_length=len(data), total=total, query_id=query_id, token=token)
        else:
            alert_message = "Sua consulta não retornou resultados para os termos indicados."
            return render_template('index.html', alert_message=alert_message)


@app.route('/download_data/<token>', methods=['GET'])
def download_data(token):
    # Retrieve the data using the token
    data_dir = os.path.join(app.config['TEMP_DATA_DIR'], token)

    if os.path.exists(data_dir):
        # Load the data from the JSON file
        with open(os.path.join(data_dir, 'data.json'), 'r') as file:
            data = json.load(file)

        # Clean up the temporary data directory
        shutil.rmtree(data_dir)

        # Return the data as JSON in the response
        response = jsonify(data)

        # Set appropriate headers for JSON download
        response.headers['Content-Disposition'] = f'attachment; filename=data.json'
        response.headers['Content-Type'] = 'application/json'

        return response
    else:
        return render_template('404.html')


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/repositrios')
def repositorios():
    return render_template('repositrios.html')


@app.route('/tecnologias')
def tecnologias():
    return render_template('tecnologias.html')


@app.route('/termos')
def termos():
    return render_template('termos.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)