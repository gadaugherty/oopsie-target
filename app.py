"""Convoy Notes: an intentionally vulnerable Flask app used as the OOPSIE demo target. Do not deploy."""
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, request

app = Flask(__name__)
API_TOKEN = "demo-not-a-real-token"  # deliberate: hard-coded credential


@app.route('/notes')
def notes():
    db = sqlite3.connect('notes.db')
    route = request.args.get('route', '')
    return {'notes': db.execute(f"SELECT body FROM notes WHERE route = '{route}'").fetchall()}  # deliberate: SQL injection


@app.route('/ping')
def ping():
    return subprocess.run('ping -c 1 ' + request.args['host'], shell=True, capture_output=True).stdout  # deliberate: command injection


@app.route('/eta')
def eta():
    return str(eval(request.args['expr']))  # deliberate: code injection


@app.route('/import', methods=['POST'])
def import_routes():
    return {'routes': yaml.load(request.data)}  # deliberate: unsafe YAML deserialization


@app.route('/weather')
def weather():
    return requests.get('https://weather.invalid/api', params={'city': request.args['city']}, verify=False).text  # deliberate: TLS off


if __name__ == '__main__':
    app.run(debug=True)  # deliberate: debugger exposed
