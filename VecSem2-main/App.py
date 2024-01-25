from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS, cross_origin
import os
import time
import urllib.request
import VecSem


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def dafault_route():
    return 'API'


@app.route('/uploadaem', methods=['POST'])
@cross_origin()
def uploadae():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        milliseconds = int(time.time() * 1000)
        filename = str(milliseconds)
        d = {}
    return d


@app.route("/get_pattern", methods=['POST'])
def get_pattern():
    msg = request.json
    print(msg)
    return []


@app.route('/getdata', methods=['POST'])
def getdata():
    #     if request.method == 'POST':
    msg = request.json
    print(msg)
    text=msg['text']
    print(text)
    data = VecSem.getData(text)
    print()
    print(data)
    return data


@app.route("/load_db", methods=['GET'])
def load_db():
    data = []
    return data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
# app.run(host="0.0.0.0")