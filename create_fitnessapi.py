# This python script creates an API by using 
# SQLite3 as its backend database

import flask
from flask import request, jsonify

import sqlite3
from sqlite3 import Error

app = flask.Flask(__name__)
app.config['DEBUG'] = True

# This function returns the output of a query 
# in the form of a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# This function initializes the Database
def initialize_db():
    connect = sqlite3.connect('fitnessfreak.db')
    return connect

# This function shows the home page of the API
@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>Welcome to the Awesome Fitness Kiosk API Home Page</h1>
    '''

# This function fetches all the data present in the database
@app.route('/v1/resources/fruits/all', methods=['GET'])
def all_data():
    connect = initialize_db()
    connect.row_factory = dict_factory
    cursor = connect.cursor()
    data = cursor.execute('''
    SELECT * FROM BMI,exercise, nutriplan , fooditem WHERE BMI.id=exercise.bmi_id AND BMI.id=nutriplan.b_id AND nutri_id=fooditem.n_id;
    ''').fetchall()

    return jsonify(data)

# This function fetches data based on the filter provided by the user
@app.route('/v1/resources/fruits/bmi', methods=['GET'])
def filterd_data():
    query_parameters = request.args

    id = query_parameters.get('id')
    name = query_parameters.get('name')
    lower = query_parameters.get('lower')
    upper = query_parameters.get('upper')

    query = 'SELECT * FROM BMI,exercise, nutriplan , fooditem WHERE BMI.id=exercise.bmi_id AND BMI.id=nutriplan.b_id AND nutri_id=fooditem.n_id AND'
    filters = []

    if name:
        query = query + ' name=? AND'
        filters.append(name)
    if not (name):
        page_not_found()
    
    # This removes everything till the fourth last character in the 
    # final query
    query = query[:-4] + ';'

    conn = initialize_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    data = cursor.execute(query, filters).fetchall()
    return jsonify(data)

# This function shows a error page if the API is not called correctly
@app.errorhandler(404)
def page_not_found():
    return '''
    <p>Ah oh, page not found :(</p>
    '''

app.run()