from flask import Flask, render_template
from explorer import Explorer

app = Flask(__name__)


def home(page_object):
    def func():
        return render_template('home.html')

    return func


# @app.route('/oiseaux')
# def oiseaux():
#     with open('content/Oiseaux/index.json') as json_file:
#         data = json.load(json_file)
#         sorted_children = sorted(data["children"], key=lambda species: species["vernacular"])
#         data["sorted_children"] = sorted_children
#         return render_template('category.html', data=data)


def species(page_object):
    def func():
        data = {**page_object.content}
        return render_template('species.html', data=data)

    return func


content = Explorer()

page_types = {
    "homepage": home,
    "species": species,
    "species_list": species,
}

for page in content.pages.values():
    view_func = page_types[page.type]
    endpoint = page.endpoint
    endpoint_name = page.endpoint_name

    app.add_url_rule(endpoint, endpoint=endpoint_name, view_func=view_func(page))
