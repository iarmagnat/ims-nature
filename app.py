from flask import Flask, render_template
from explorer import Page, init_explorer, slugify

app = Flask(__name__)


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
        return render_template('species.html', data=data)

    return func


page_types = {
    "species": SpeciesPage,
    "species_list": CategoryPage,
}

page_funcs = {
    "homepage": home,
    "species": species,
    "species_list": species_list,
}

init_explorer(app, page_funcs, page_types=page_types)
