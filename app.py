from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from WebWeaver import webweaver
import logging

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/webweaver'
mongo = PyMongo(app)
logging.basicConfig(filename='webweaver.log', level=logging.DEBUG)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    global data
    if request.method == 'POST':
        # Access form data using request.form
        repository = request.form['repository']
        query_type = request.form['query_type']
        year = request.form['year']
        search_terms = request.form['search_terms']

        logging.debug(f"Repository: {repository}")
        logging.debug(f"Query Type: {query_type}")
        logging.debug(f"Year: {year}")
        logging.debug(f"Search Terms: {search_terms}")

        webweaver(repository, search_terms, query_type, year)

        # Define a dictionary to map repository choices to MongoDB collection names
        repository_collections = {
            "1": "wos",
            "2": "els",
            "3": "bdtd",
        }

        search_terms = search_terms.replace(' ', '+')

        if repository in repository_collections:
            collection_name = f'{search_terms}_{year}_{repository_collections[repository]}'
            data_collection = mongo.db[collection_name]

            data = data_collection.find()
        else:
            collection_wos = f'{search_terms}_{year}_wos'
            collection_els = f'{search_terms}_{year}_els'
            collection_bdtd = f'{search_terms}_{year}_bdtd'

            data_wos = list(mongo.db[collection_wos].find())
            data_els = list(mongo.db[collection_els].find())
            data_bdtd = list(mongo.db[collection_bdtd].find())

            # Concatenate the data from all three collections into a single list
            data = data_wos + data_els + data_bdtd

    return render_template('data.html', data=data)


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
