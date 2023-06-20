from flask import Flask, request
from scraper import scrapit
from analyzer import analyzeit
import json
import os

app = Flask(__name__)


@app.route('/api/scrap', methods=['GET'])
def scrap():
    product_code = request.args.get("product_code")
    if str(product_code) in str(os.listdir('opinions')):
        with open(f'opinions/{product_code}.json', 'r', encoding='utf-8') as f:
            x = json.load(f)
            return x
    else:
        return scrapit(product_code)


@app.route('/api/stats', methods=['GET'])
def stats():
    product_code = request.args.get("product_code")
    data = analyzeit(product_code)

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response


app.run()
