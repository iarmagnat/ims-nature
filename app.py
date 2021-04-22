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


@app.route('/oiseaux')
def oiseaux():
    with open('content/Oiseaux/index.json') as json_file:
        data = json.load(json_file)
        sorted_children = sorted(data["children"], key=lambda species: species["vernacular"])
        data["sorted_children"] = sorted_children
        return render_template('category.html', data=data)


@app.route('/pwet')
def home2():
    return 'pwet'
