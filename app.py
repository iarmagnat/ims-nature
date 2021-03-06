from collections import defaultdict, OrderedDict

from flask import Flask, render_template, current_app
from explorer import Page, init_explorer, slugify

app = Flask(__name__)

app.config["SERVER_NAME"] = "127.0.0.1:5000"


def tree():
    return defaultdict(tree)


taxonomy_order = (
    "Règne",
    "Embranchement",
    "Sous-embranchement",
    "Classe",
    "Ordre",
    "Famille",
    "Genre",
    "Espèce"
)


@app.template_filter("use_sm")
def use_sm(text):
    return "_sm.".join(text.split("."))


class SpeciesPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default Meta-description if needed
        if not self.metadata.get("meta_description"):
            meta_desc = f"Quelques informations et photos de {self.usable_name}."
            self.metadata["meta_description"] = meta_desc
            self.content["metadata"]["meta_description"] = meta_desc

    @property
    def usable_name(self):
        if self.content.get("vernacular"):
            return self.content["vernacular"]
        else:
            return self.content["name"]

    @property
    def vernacular(self):
        if self.content.get("vernacular"):
            return self.content["vernacular"]
        else:
            return ""

    @property
    def taxonomy(self):
        return OrderedDict(**self.content["taxonomy"])


class CategoryPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata["menu_title"] = self.content["category_name"]

        # Set default Meta-description if needed
        if not self.metadata.get("meta_description"):
            meta_desc = f"Liste des {self.content['category_name']} sur le site."
            self.metadata["meta_description"] = meta_desc
            self.content["metadata"]["meta_description"] = meta_desc


def home(page_object):
    def func():
        return render_template('home.html')

    return func


def dendrogram(page_object):
    def func():
        data = tree()
        for page in current_app.explorer.pages.values():
            if page.type == "species":
                taxonomy = page.content["taxonomy"]
                # current data is a cursor that is used to discover the whole tree up to the point of the page
                current_data = data
                for index, taxon in enumerate(taxonomy_order):
                    if index == len(taxonomy_order) - 1:
                        current_data[taxonomy[taxon]] = page
                    else:
                        current_data = current_data[taxonomy[taxon]]

        return render_template('dendrogram.html', taxonomy_order=taxonomy_order, data=data)

    return func


def species_list(page_object):
    def func():
        def mapper(item):
            content = {**item.content}
            content["usable_name"] = item.usable_name
            content["endpoint"] = item.endpoint
            return content

        neighbour_pages = filter(lambda item: item.type == "species", page_object.parent.child_pages)
        sorted_children = map(mapper, neighbour_pages)
        sorted_children = sorted(sorted_children, key=lambda item: slugify(item["usable_name"]))
        return render_template('category.html', data={"sorted_children": sorted_children, **page_object.content})

    return func


def species(page_object):
    def func():
        data = {**page_object.content}
        return render_template('species.html', data=data, taxonomy=page_object.taxonomy)

    return func


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

page_types = {
    "species": SpeciesPage,
    "species_list": CategoryPage,
}

page_funcs = {
    "homepage": home,
    "species": species,
    "species_list": species_list,
    "dendrogram": dendrogram,
}

init_explorer(app, page_funcs, page_types=page_types)
