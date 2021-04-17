from flask import Flask, render_template

import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/huppe')
def huppe():
    with open('content/Oiseaux/huppe.json') as json_file:
        data = json.load(json_file)
        return render_template('species.html', data=data)


@app.route('/pwet')
def home2():
    return 'pwet'
