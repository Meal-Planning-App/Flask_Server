from flask import Flask, request, jsonify
from ml.GeneticAlgorithm2 import GeneticAlgorithm

import os, sys

import urllib.request, json

database = None

with urllib.request.urlopen('https://api.myjson.com/bins/13jaom') as url:
    database = json.loads(url.read().decode())
    # print(str(database).encode(sys.stdout.encoding, errors='replace'))
    print(r'Database was loaded!!!')

fileDir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
ga = GeneticAlgorithm()

@app.route('/')
def hello():
    return 'This is your python server'

@app.route('/get_recipes', methods=['GET', 'POST'])
def recipes_list():
    content = request.json["data"]
    data = []
    for i in range(len(content)):
        _, data_dict = ga.run_algorithm(database, content[str(i)])
        data.append(data_dict)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
