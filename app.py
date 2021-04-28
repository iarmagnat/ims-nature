from flask import Flask, render_template
from explorer import Explorer

import json

app = Flask(__name__)


# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.add_url_rule

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


content = Explorer()


@app.route("/dump")
def dump():
    return render_template("dump.html", content=json.dumps(content))
